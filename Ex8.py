from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

n_est = int(input("Enter number of estimators (n_estimators): "))
crit = input("Enter criterion (gini or entropy): ")
data = load_breast_cancer()
X = data.data
y = data.target

split_ratios = [0.30, 0.40, 0.25]
split_names = ["70-30", "60-40", "75-25"]
final_results = []

for i in range(len(split_ratios)):
    print("\n--------------------------------------------")
    print("Split:", split_names[i])
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=split_ratios[i],random_state=42)
    print("Train samples:", len(X_train))
    print("Test samples :", len(X_test))
    rf = RandomForestClassifier(n_estimators=n_est, criterion=crit, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    TN = cm[0][0]
    FP = cm[0][1]
    FN = cm[1][0]
    TP = cm[1][1]
    print("\nConfusion Matrix:")
    print("          Predicted 0   Predicted 1")
    print("Actual 0     TN=", TN, "   FP=", FP)
    print("Actual 1     FN=", FN, "   TP=", TP)

    accuracy = round(accuracy_score(y_test, y_pred), 4)
    precision = round(precision_score(y_test, y_pred), 4)
    recall = round(recall_score(y_test, y_pred), 4)
    f1 = round(f1_score(y_test, y_pred), 4)
    print("\nAccuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1 Score :", f1)
    final_results.append([split_names[i], TP, TN, FP, FN, accuracy, precision, recall, f1])

print("\n\nFinal Consolidated Results:")
print("Split   TP   TN   FP   FN   Accuracy  Precision  Recall   F1-Score")
for row in final_results:
    print(f"{row[0]:6} {row[1]:3}  {row[2]:3}  {row[3]:3}  {row[4]:3}   {row[5]:8}   {row[6]:8}   {row[7]:8}   {row[8]:8}")
