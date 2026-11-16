import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
from sklearn.model_selection import train_test_split

project_root=Path(__file__).resolve().parents[1]
data_path=project_root/"data"/"processed"/"database_activity_processed.csv"
df=pd.read_csv(data_path)
X=df.drop(columns=["anomaly_label"])
y=df["anomaly_label"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
X_train_normal=X_train[y_train==0]
contamination_values=["auto",0.02,0.05]
results=[]

print("\n========== MODEL EVALUATION ==========")
print("Total dataset records:",len(df))
print("Training records:",len(X_train_normal))
print("Testing records:",len(X_test))
for contamination in contamination_values:
    model=IsolationForest(n_estimators=100,contamination=contamination,random_state=42)
    model.fit(X_train_normal)
    raw_predictions=model.predict(X_test)
    predictions=[1 if value==-1 else 0 for value in raw_predictions]
    accuracy=accuracy_score(y_test,predictions)
    matrix=confusion_matrix(y_test,predictions,labels=[0,1])
    report=classification_report(y_test,predictions,labels=[0,1],target_names=["Normal","Anomaly"],output_dict=True,zero_division=0)
    results.append({"contamination":str(contamination),"accuracy":accuracy,"precision":report["Anomaly"]["precision"],"recall":report["Anomaly"]["recall"],"f1_score":report["Anomaly"]["f1-score"]})
    print("\n========================================")
    print("CONTAMINATION:",contamination)
    print("========================================")
    print("Accuracy:",round(accuracy,4))
    print("\nConfusion Matrix:")
    print(matrix)
    print("\nClassification Report:")
    print(classification_report(y_test,predictions,labels=[0,1],target_names=["Normal","Anomaly"],zero_division=0))
results_df=pd.DataFrame(results)
print("\n========== CONFIGURATION COMPARISON ==========")
print(results_df.to_string(index=False))
output_path=project_root/"data"/"processed"/"model_evaluation_comparison.csv"
results_df.to_csv(output_path,index=False)
print("\nComparison saved at:",output_path)
print("\nMODEL EVALUATION COMPLETED!")