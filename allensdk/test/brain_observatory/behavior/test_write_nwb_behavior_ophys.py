import pytest
import pandas as pd
import numpy as np

import allensdk.brain_observatory.nwb as nwb
from allensdk.brain_observatory.behavior.behavior_ophys_api.behavior_ophys_nwb_api import BehaviorOphysNwbApi


@pytest.mark.parametrize('roundtrip', [True, False])
def test_add_running_speed_to_nwbfile(nwbfile, running_speed, roundtrip, roundtripper):

    nwbfile = nwb.add_running_speed_to_nwbfile(nwbfile, running_speed)

    if roundtrip:
        obt = roundtripper(nwbfile, BehaviorOphysNwbApi)
    else:
        obt = BehaviorOphysNwbApi.from_nwbfile(nwbfile)

    running_speed_obt = obt.get_running_speed()
    assert np.allclose(running_speed.timestamps, running_speed_obt.timestamps)
    assert np.allclose(running_speed.values, running_speed_obt.values)


@pytest.mark.parametrize('roundtrip', [True, False])
def test_add_running_data_df_to_nwbfile(nwbfile, running_data_df, roundtrip, roundtripper):

    unit_dict = {'v_sig': 'V', 'v_in': 'V', 'speed': 'cm/s', 'timestamps': 's', 'dx': 'cm'}
    nwbfile = nwb.add_running_data_df_to_nwbfile(nwbfile, running_data_df, unit_dict)

    if roundtrip:
        obt = roundtripper(nwbfile, BehaviorOphysNwbApi)
    else:
        obt = BehaviorOphysNwbApi.from_nwbfile(nwbfile)

    pd.testing.assert_frame_equal(running_data_df, obt.get_running_data_df())


@pytest.mark.parametrize('roundtrip', [True, False])
def test_add_stimulus_templates(nwbfile, stimulus_templates, roundtrip, roundtripper):
    for key, val in stimulus_templates.items():
        nwb.add_stimulus_template(nwbfile, val, key)

    if roundtrip:
        obt = roundtripper(nwbfile, BehaviorOphysNwbApi)
    else:
        obt = BehaviorOphysNwbApi.from_nwbfile(nwbfile)

    stimulus_templates_obt = obt.get_stimulus_templates()
    for key in set(stimulus_templates.keys()).union(set(stimulus_templates_obt.keys())):
        np.testing.assert_array_almost_equal(stimulus_templates[key], stimulus_templates_obt[key])


@pytest.mark.parametrize('roundtrip', [True, False])
def test_add_stimulus_presentations(nwbfile, stimulus_presentations, roundtrip, roundtripper):
    nwb.add_stimulus_presentations(nwbfile, stimulus_presentations)

    if roundtrip:
        obt = roundtripper(nwbfile, BehaviorOphysNwbApi)
    else:
        obt = BehaviorOphysNwbApi.from_nwbfile(nwbfile)

    pd.testing.assert_frame_equal(stimulus_presentations, obt.get_stimulus_presentations(), check_dtype=False)