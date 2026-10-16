"""Offline regression of actual app AST; no real key, prompt or financial data."""
import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import unittest

SOURCE = Path(__file__).with_name('app.py').read_text(encoding='utf-8')
TREE = ast.parse(SOURCE)
STABLE = ['gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-2.5-flash']


class State(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def policy_namespace():
    assignments = [n for n in TREE.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id in {'DEFAULT_MODELS', 'session_defaults'}
                           for t in n.targets)]
    ns = {}
    exec(compile(ast.Module(body=assignments, type_ignores=[]), 'app.py', 'exec'), ns)
    ns['st'] = SimpleNamespace(session_state=State(model_name=STABLE[0], api_key_valid=False,
                                                available_models=STABLE.copy(), api_error=None))
    client = Mock()
    ns['get_gemini_client'] = lambda key: client
    functions = [n for n in TREE.body if isinstance(n, ast.FunctionDef)
                 and n.name == 'validate_and_discover_gemini']
    exec(compile(ast.Module(body=functions, type_ignores=[]), 'app.py', 'exec'), ns)
    return ns, client


class ModelPolicyTests(unittest.TestCase):
    def setUp(self):
        self.block_network = patch('socket.socket', side_effect=AssertionError('OFFLINE_ONLY'))
        self.block_network.start()
        self.addCleanup(self.block_network.stop)
        self.ns, self.client = policy_namespace()

    def test_default_is_supported_stable_and_simulation_remains_keyless(self):
        self.assertEqual(self.ns['DEFAULT_MODELS'], STABLE)
        self.assertEqual(self.ns['session_defaults']['model_name'], STABLE[0])
        self.assertTrue(self.ns['session_defaults']['simulation_mode'])
        self.assertFalse(self.ns['session_defaults']['api_key_valid'])

    def test_metadata_failure_does_not_generate_ping_or_retain_authorization(self):
        self.ns['st'].session_state.api_key_valid = True
        self.client.models.list.side_effect = RuntimeError('SYNTHETIC_SECRET')
        self.assertFalse(self.ns['validate_and_discover_gemini']('synthetic'))
        self.assertFalse(self.ns['st'].session_state.api_key_valid)
        self.client.models.generate_content.assert_not_called()
        self.assertNotIn('SYNTHETIC_SECRET', str(self.ns['st'].session_state.api_error))

    def test_empty_list_fails_closed_without_generation(self):
        self.client.models.list.return_value = []
        self.assertFalse(self.ns['validate_and_discover_gemini']('synthetic'))
        self.client.models.generate_content.assert_not_called()

    def test_only_supported_text_generation_models_in_preferred_order(self):
        self.client.models.list.return_value = [
            SimpleNamespace(name='models/gemini-4-argon-preview', supported_actions=['generateContent']),
            SimpleNamespace(name='models/gemini-1.5-flash', supported_actions=['generateContent']),
            SimpleNamespace(name='models/gemini-2.0-flash', supported_actions=['generateContent']),
            SimpleNamespace(name='models/gemini-2.5-flash', supported_actions=['generateContent']),
            SimpleNamespace(name='models/gemini-3.5-flash-lite', supported_actions=['generateContent']),
            SimpleNamespace(name='models/gemini-3.8-flash', supported_actions=['embedContent'])]
        self.assertTrue(self.ns['validate_and_discover_gemini']('synthetic'))
        self.assertEqual(self.ns['st'].session_state.available_models, STABLE[1:])
        self.assertEqual(self.ns['st'].session_state.model_name, STABLE[1])
        self.client.models.generate_content.assert_not_called()

    def test_legacy_action_metadata_is_supported_without_legacy_models(self):
        self.client.models.list.return_value = [SimpleNamespace(
            name='models/gemini-3.8-flash', supported_generation_methods=['generateContent'])]
        self.assertTrue(self.ns['validate_and_discover_gemini']('synthetic'))
        self.assertEqual(self.ns['st'].session_state.available_models, [STABLE[0]])
        self.client.models.generate_content.assert_not_called()

    def test_explicit_empty_supported_actions_is_not_generation_eligible(self):
        self.client.models.list.return_value = [SimpleNamespace(
            name='models/gemini-3.8-flash', supported_actions=[])]
        self.assertFalse(self.ns['validate_and_discover_gemini']('synthetic'))
        self.client.models.generate_content.assert_not_called()

    def test_stale_session_loses_retired_model_authorization(self):
        state = State(model_name='gemini-1.5-flash', api_key_valid=True,
                      available_models=['gemini-1.5-flash'], simulation_mode=False)
        ns = dict(self.ns, st=SimpleNamespace(session_state=state))
        start = next(i for i, n in enumerate(TREE.body) if isinstance(n, ast.For)
                     and ast.unparse(n.iter) == 'session_defaults.items()')
        end = next(i for i in range(start + 1, len(TREE.body))
                   if isinstance(TREE.body[i], ast.FunctionDef))
        exec(compile(ast.Module(body=TREE.body[start:end], type_ignores=[]), 'app.py', 'exec'), ns)
        self.assertEqual(state.model_name, STABLE[0])
        self.assertEqual(state.available_models, STABLE)
        self.assertFalse(state.api_key_valid)
        self.assertTrue(state.simulation_mode)


if __name__ == '__main__':
    unittest.main()
