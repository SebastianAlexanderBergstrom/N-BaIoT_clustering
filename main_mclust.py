from util import * 

random.seed(11)
base_directory = ''

# temporary comment out since it's done
create_data_frames(base_directory + 'DanminiDoorbell/',0.9,False,True)
create_data_frames(base_directory + 'EcobeeThermostat/',0.9,False,True)
create_data_frames(base_directory + 'EnnioDoorbell/',0.9,False,True)
create_data_frames(base_directory + 'PhilipsBabyMonitor/',0.9,False,True)
create_data_frames(base_directory + 'ProvisionPT737ESecurityCamera/',0.9,False,True)
create_data_frames(base_directory + 'ProvisionPT838SecurityCamera/',0.9,False,True)
create_data_frames(base_directory + 'SamsungSNHWebcam/',0.9,False,True)
create_data_frames(base_directory + 'SimpleHomeXCS71002WHTSecurityCamera/',0.9,False,True)
create_data_frames(base_directory + 'SimpleHomeXCS71003WHTSecurityCamera/',0.9,False,True)

#run main.R before running the run_mixture_analysis() calls

run_mixture_analysis(base_directory+'DanminiDoorbell/'
                           , 'DanminiDoorbell_labels_and_assignments.csv'
                           , 'DanminiDoorbell_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'EcobeeThermostat/'
                           , 'EcobeeThermostat_labels_and_assignments.csv'
                           , 'EcobeeThermostat_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'EnnioDoorbell/'
                           , 'EnnioDoorbell_labels_and_assignments.csv'
                           , 'EnnioDoorbell_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'PhilipsBabyMonitor/'
                           , 'PhilipsBabyMonitor_labels_and_assignments.csv'
                           , 'PhilipsBabyMonitor_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'ProvisionPT737ESecurityCamera/'
                           , 'ProvisionPT737ESecurityCamera_labels_and_assignments.csv'
                           , 'ProvisionPT737ESecurityCamera_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'ProvisionPT838SecurityCamera/'
                           , 'ProvisionPT838SecurityCamera_labels_and_assignments.csv'
                           , 'ProvisionPT838SecurityCamera_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'SamsungSNHWebcam/'
                           , 'SamsungSNHWebcam_labels_and_assignments.csv'
                           , 'SamsungSNHWebcam_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'SimpleHomeXCS71002WHTSecurityCamera/'
                           , 'SimpleHomeXCS71002WHTSecurityCamera_labels_and_assignments.csv'
                           , 'SimpleHomeXCS71002WHTSecurityCamera_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')
run_mixture_analysis(base_directory+'SimpleHomeXCS71003WHTSecurityCamera/'
                           , 'SimpleHomeXCS71003WHTSecurityCamera_labels_and_assignments.csv'
                           , 'SimpleHomeXCS71003WHTSecurityCamera_best_model_info.csv'
                           , 0.9
                           , 'MCLUST')