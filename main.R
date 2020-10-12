library(mclust)
library(clusterSim)

# Functions used ----------------------------------------------------------

select_nr_of_clusters_for_model <- function(model_name,data_frame, nr_of_clusters_vector,model_family){
  db_scores <- c(numeric(length(nr_of_clusters_vector)))
  for(nr_of_clusters in nr_of_clusters_vector){
    tryCatch(
      {
        print(paste0("Using ", nr_of_clusters, " clusters"))
        if(model_family == "MCLUST"){
          fitted_model <- Mclust(data_frame,G=nr_of_clusters,modelNames=model_name)
          #db_scores[nr_of_clusters-1] <- index.DB(data_frame,fitted_model$classification)$DB
        }
        else if(model_family == "tEIGEN"){
          fitted_model <- teigen(data_frame,G=nr_of_clusters,models=model_name)
          #db_scores[nr_of_clusters-1] <- index.DB(data_frame,fitted_model$classification)$DB
        }
        db_scores[nr_of_clusters-1] <- index.DB(data_frame,fitted_model$classification)$DB
      },
      warning = function(w){print("warning message")},
      error = function(e){print(paste0("Model fitting and/or Davies-Bouldin computation failed for the model ",model_name))},
      finally = {}
    )
  }
  # problem if fitted_model doesn't exist
  if(is.null(fitted_model)){
    return(-1)
  }
  else{
    minimum_db_nr_of_clusters <- which.min(db_scores)+1
    return(minimum_db_nr_of_clusters)
  }
}

select_best_model <- function(model_names_vector,data_frame,nr_of_clusters_vector,model_family){
  n <- length(model_names_vector)
  models_information_list <- vector("list",n)
  for(i in 1:n){
    model_name <- model_names_vector[i]
    print(paste0("starting with model", " ", model_name))
    optimal_nr_of_clusters_for_model <- select_nr_of_clusters_for_model(model_name
                                                                        , data_frame
                                                                        , nr_of_clusters_vector
                                                                        , model_family)
    if(optimal_nr_of_clusters_for_model == -1){
      models_information_list[[i]] <- list(model_name = model_name
                                           , optimal_nr_of_clusters_for_model = NA
                                           , optimal_db_score_for_model = NA) 
    }
    else{
      if(model_family == "MCLUST"){
        optimal_model_specification <- Mclust(data_frame
                                              , G=optimal_nr_of_clusters_for_model
                                              , modelNames=model_name)
        
      }
      else if(model_family == "tEIGEN"){
        optimal_model_specification <- teigen(data_frame
                                              , G=optimal_nr_of_clusters_for_model
                                              , models=model_name)
      }
      optimal_db_score_for_model <- index.DB(data_frame
                                             , optimal_model_specification$classification)$DB
      models_information_list[[i]] <- list(model_name = model_name
                                           , optimal_nr_of_clusters_for_model = optimal_nr_of_clusters_for_model
                                           , optimal_db_score_for_model = optimal_db_score_for_model)
      
    }
    
  }
  
  model_summary_data_frame = as.data.frame(do.call(rbind, lapply(models_information_list, unlist)))
  model_summary_data_frame <- model_summary_data_frame[which(!is.na(model_summary_data_frame$optimal_nr_of_clusters_for_model)),]
  if(nrow(model_summary_data_frame) == 0){
    return(-1)
  }
  else{
    best_model <- model_summary_data_frame[which(model_summary_data_frame$optimal_db_score_for_model == min(model_summary_data_frame$optimal_db_score_for_model)),]
    return(best_model)
  }
}


# Computations ------------------------------------------------------------
device_name_vector <- c("DanminiDoorbell"
                  ,"EcobeeThermostat"
                  ,"EnnioDoorbell"
                  ,"PhilipsBabyMonitor"
                  ,"ProvisionPT737ESecurityCamera"
                  ,"ProvisionPT838SecurityCamera"
                  ,"SamsungSNHWebcam"
                  ,"SimpleHomeXCS71002WHTSecurityCamera"
                  ,"SimpleHomeXCS71003WHTSecurityCamera")
mclust_model_names <- mclust.options("emModelNames")
nr_of_mclust_models <- length(mclust_model_names)

for(device_name in device_name_vector){
  print(device_name)
  path <- paste0("",device_name,"\\",device_name,"_pca",".csv") # read the "_pca.csv"-files created from the Python-script
  device_data <- read.csv(path)
  device_data <- subset(device_data,select=-c(X,label))
  mclust_best_model <- select_best_model(mclust_model_names, device_data,2:11,"MCLUST")
  
  if(mclust_best_model == -1){
    message_string <- paste0("For ", device_name, " no MCLUST models converged")
  }
  else{
    mclust_fitted_best_model <- Mclust(device_data,
                                       G = mclust_best_model$optimal_nr_of_clusters_for_model,
                                       modelNames = mclust_best_model$model_name)
    device_data$cluster_assignment <- mclust_fitted_best_model$classification
    
    write.csv(device_data,paste0("",device_name,"\\",device_name,"_labels_and_assignments.csv"),row.names=FALSE)
    write.csv(mclust_best_model,paste0("",device_name,"\\",device_name,"_best_model_info.csv"),row.names=FALSE)
  }

}
