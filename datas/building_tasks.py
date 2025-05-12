
from utils.load_json import load_json
from utils.save_json import save_json
from utils.find_diverse_party import max_variance_parties
from utils.allocate_weights import allocate_weights
from utils.sample_data import sampling_data
from datas.task_infos import topic_list, party_num_settings

for party_num in party_num_settings:
    for topic_name in topic_list:
        datas = load_json(f'topic_datas/{topic_name}.json')
        task_datas = []
        for data_id, data in enumerate(datas):
            if len(data['stances']) < int(party_num):
                continue
            tmp_stances = []
            if party_num == '2':
                tmp_stances = max_variance_parties(data['stances'], 2)
            elif party_num == '4':
                tmp_stances = max_variance_parties(data['stances'], 4)
            elif party_num == '6':
                tmp_stances = max_variance_parties(data['stances'], 6)
            else:  
                party_num = 'all'
                if len(data['stances']) == 0:
                    continue
                tmp_stances = data['stances']

            data['id'] = data_id
            data['stances'] = tmp_stances
            data['seat_weights'] = allocate_weights(tmp_stances)
            data['veto_party_name'] = sampling_data(data['stances'], 1)[0]['party_name']
            task_datas.append(data)
        save_json(task_datas, f'task_datas/{party_num}/{topic_name}.json')
                    
                    