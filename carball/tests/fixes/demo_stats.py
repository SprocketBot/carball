import unittest
from carball.analysis.analysis_manager import AnalysisManager
from carball.tests.utils import run_analysis_test_on_replay, get_raw_replays


class Test_CameraSettings:

    def test_player_platforms(self, replay_cache):
        
        def test(analysis: AnalysisManager):
            proto_game = analysis.get_protobuf_data()
            player1 = proto_game.players[0]
            demos = player.demos

            assert len(demos) == 20

        run_analysis_test_on_replay(test, get_raw_replays()["MANY_DEMOS_NEW"], cache=replay_cache)
