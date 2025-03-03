# -*- coding: utf-8 -*-
"""DSCI441_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NxQxfmYBfNEY-ubXrCon5zWqAkow-SmD
"""

# Importing the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from scipy.stats import t
from scipy.stats import f_oneway
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor

# Loading the data
data = pd.read_csv("insurance_data.csv")
data.head(5)

# Check age distribution for seniors
print(data[data['Is_Senior'] == 1]['Age'].describe())

# Check age distribution for non-seniors
print(data[data['Is_Senior'] == 0]['Age'].describe())

data['Is_Senior'] = np.where(data['Age'] >= 55, 1, 0)

"""# Data Exploration"""

# Data Preprocessing
rows, cols = data.shape
attributes = data.columns.tolist()
print("Number of rows and columns:", rows, cols)
print("Attributes:", attributes)

# Missing Values
print(f"Total missing values: {data.isna().sum().sum()}")

# Duplicate Rows
print(f"Total duplicate rows: {data.duplicated().sum()}")

# Data Structure
print(data.info())

# Statistical Analysis
print(data.describe())

# Categorical Feature Analysis
categorical_features = data.select_dtypes(include=['object']).nunique()
print("Unique values per categorical feature:")
print(categorical_features)

"""# Exploratory Data Analysis

**Univariate Analysis**
"""

# Plot histograms for numerical features
numerical_features = ['Age', 'Claims_Frequency', 'Claims_Severity', 'Credit_Score']
for feature in numerical_features:
    plt.figure(figsize=(8, 4))
    sns.histplot(data[feature], kde=True, bins=30)
    plt.title(f'Distribution of {feature}')
    plt.show()

"""**Bivariate Analysis**"""

# Plot boxplots to check for outliers
for feature in numerical_features:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=data[feature])
    plt.title(f'Boxplot of {feature}')
    plt.show()

categorical_features = ['Marital_Status', 'Policy_Type', 'Region']
for feature in categorical_features:
    plt.figure(figsize=(8, 4))
    sns.countplot(x=data[feature], order=data[feature].value_counts().index)
    plt.title(f'Distribution of {feature}')
    plt.xticks(rotation=45)
    plt.show()

# Scatterplots for numerical features vs. Premium_Amount
for feature in numerical_features:
    plt.figure(figsize=(8, 4))
    sns.scatterplot(x=data[feature], y=data['Premium_Amount'])
    plt.title(f'{feature} vs. Premium_Amount')
    plt.show()

"""1. Age
-> Observation: Premiums are equally distributed across age groups, but there are specific data points at ages 20, 30, 40, 50, and 60 with premiums around 2800.

-> Insight: Age alone may not be a strong predictor of premiums, but the spikes at specific ages (e.g., 20, 30, 40, 50, 60) suggest that certain age thresholds might influence premiums. This could be due to policy rules or discounts applied at these ages.

2. Claims Frequency
-> Observation: Claims frequency is evenly distributed, but claims frequencies of 2 and 3 tend to have higher premiums (reaching 2800). A claims frequency of 5 has only a few data points in the middle range.

-> Insight: Higher claims frequencies (2 and 3) are associated with higher premiums, which makes sense—customers with more claims are riskier to insure. However, the relationship isn’t perfectly linear, as a claims frequency of 5 doesn’t show the highest premiums. This could indicate that other factors (e.g., claims severity, discounts) are also at play.

3. Claims Severity
-> Observation: Higher claims severity is associated with higher premiums, but the distribution is even.

-> Insight: This is expected—more severe claims lead to higher premiums. However, the even distribution suggests that claims severity alone isn’t the sole driver of premiums. Other factors (e.g., policy type, discounts) might moderate this relationship.
"""

for feature in categorical_features:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=data[feature], y=data['Premium_Amount'])
    plt.title(f'{feature} vs. Premium_Amount')
    plt.xticks(rotation=45)
    plt.show()

"""1. Policy Type
-> Observation: Liability-only policies have higher quartiles (75th percentile) compared to full-coverage policies, but the overall spread (length of the boxplot) and number of outliers are similar.

-> Insight: This is counterintuitive—typically, full-coverage policies are more expensive. This could indicate:

- Liability-only policies are chosen by higher-risk drivers, leading to higher premiums. There might be interactions with other features (e.g., discounts, region) that influence premiums differently for each policy type.

2. Region
-> Observation: Premiums are significantly higher in urban areas.

-> Insight: This is expected—urban areas typically have higher risk (e.g., more traffic, higher likelihood of accidents or theft), leading to higher premiums. This feature is likely to be a strong predictor in your model.

# Correlation Analysis
"""

# Identify numerical columns
numerical_data = data.select_dtypes(include=np.number)

# Calculate the correlation matrix
correlation_matrix = numerical_data.corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Correlation with Premium_Amount
correlation_with_target = correlation_matrix['Premium_Amount'].abs().sort_values(ascending=False)
print(correlation_with_target)

"""Correlation values range from **-1 to 1**, where:  
- **1**: Perfect positive correlation (variables move in the same direction).  
- **-1**: Perfect negative correlation (variables move in opposite directions).  
- **0**: No linear relationship.  

Here are the **key insights** from the above matrix:

**1. Strong Correlations to Focus On**  
**Premium_Amount** (the target variable?):  
- **Policy_Adjustment (0.66)**: Strong positive correlation. Adjustments to policies (e.g., coverage changes) likely drive higher premiums.  
- **Claims_Adjustment (0.44)**: Higher claim adjustments correlate with higher premiums.  
- **Credit_score (-0.25)**: Negative correlation. Lower credit scores may lead to higher premiums.  
- **Premium_Adjustment_Region (0.27)**: Regional factors slightly influence premiums.  

**Claims_Frequency & Claims_Adjustment (0.80)**:  
- Very strong positive correlation. Frequent claims lead to more claim adjustments (expected).  

**Credit_score & Premium_Adjustment_Credit (-0.79)**:  
- Strong negative correlation. Credit scores heavily influence credit-based premium adjustments.  

**Conversion_Status & Time_to_Conversion (-1.00)**:  
- *Perfect correlation* (likely a data issue).

**2. Unexpected or Odd Correlations**  
- **Premium_Amount & Safe_Driver_Discount (-0.13)**:  
  - Slight negative correlation. Safe drivers might receive discounts, lowering premiums. This aligns with intuition.  

- **Total_Discounts & Premium_Amount (-0.23)**:  
  - Negative correlation. More discounts reduce premiums (expected).  

**3. Multicollinearity Warnings**  
Variables with **|r| > 0.7** may cause multicollinearity in regression models. Consider:  
- **Claims_Frequency & Claims_Adjustment (0.80)**  
- **Credit_score & Premium_Adjustment_Credit (0.79)**  
- **Policy_Adjustment & Premium_Amount (0.66)**  

**Action**: Remove one variable from each pair or use techniques like PCA.  

**4. Weak or No Relationships**  
- **Website_Visits & Premium_Amount (0.02)**: Almost no correlation.  
- **Inquiries & Premium_Amount (0.00)**: No linear relationship.

# Principal Component Analysis
"""

from sklearn.decomposition import PCA

# Apply PCA to Claims_Frequency & Claims_Adjustment
pca_claims = PCA(n_components=1)
data['Claims_PCA'] = pca_claims.fit_transform(data[['Claims_Frequency', 'Claims_Adjustment']])

# Apply PCA to Credit_Score & Premium_Adjustment_Credit
pca_credit = PCA(n_components=1)
data['Credit_PCA'] = pca_credit.fit_transform(data[['Credit_Score', 'Premium_Adjustment_Credit']])

# Drop the original multicollinear columns
data_reduced = data.drop(columns=[
    'Claims_Frequency', 'Claims_Adjustment',  # Replaced by Claims_PCA
    'Credit_Score', 'Premium_Adjustment_Credit'  # Replaced by Credit_PCA
])

from sklearn.preprocessing import StandardScaler

# Standardize the data before PCA
scaler = StandardScaler()
scaled_claims = scaler.fit_transform(data[['Claims_Frequency', 'Claims_Adjustment']])
pca_claims = PCA(n_components=1)
pca_claims.fit(scaled_claims)
print("Standardized Claims_PCA Loadings:", pca_claims.components_)

# Check PCA loadings for Claims_PCA
print("Claims_PCA Loadings:")
print(pca_claims.components_)

# Check PCA loadings for Credit_PCA
print("Credit_PCA Loadings:")
print(pca_credit.components_)

# Identify numerical columns
numerical_data_pca = data_reduced.select_dtypes(include=np.number)

# Calculate the correlation matrix
correlation_matrix_pca = numerical_data_pca.corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix_pca, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Correlation with Premium_Amount
correlation_with_target_pca = correlation_matrix_pca['Premium_Amount'].abs().sort_values(ascending=False)
print(correlation_with_target_pca)

# Removing features with weak correlations
data_final = data_reduced.drop(columns=[
    'Website_Visits', 'Inquiries', 'Time_Since_First_Contact',
    'Quotes_Requested', 'Is_Senior'
])
print(data_final.columns)

"""# Hypothesis Testing"""

#T-Test for Binary Groups (Married_Premium_Discount)
# Split data into two groups
married_premiums = data_final[data_final['Married_Premium_Discount'] == 86]['Premium_Amount']
unmarried_premiums = data_final[data_final['Married_Premium_Discount'] == 0]['Premium_Amount']

# Perform t-test
t_stat, p_value = ttest_ind(married_premiums, unmarried_premiums)
print(f"T-Statistic: {t_stat}, P-Value: {p_value}")

"""**T-Test for Binary Groups (Married_Premium_Discount)**

Correlation with Target Variable: 0.29

Objective: Test if there’s a significant difference in premiums between married and unmarried individuals.

Hypotheses:

- Null Hypothesis (H₀): There is no significant difference in premiums between married and unmarried individuals.

- Alternative Hypothesis (H₁): There is a significant difference in premiums between married and unmarried individuals.

**Interpretation:**

The p-value is extremely small (much less than 0.05), so we reject the null hypothesis.

This means there is a statistically significant difference in premiums between married and unmarried individuals.

The positive T-statistic suggests that married individuals tend to have higher premiums than unmarried individuals.

*Action:
Including Married_Premium_Discount in my model, as it significantly impacts premiums.*
"""

#ANOVA for Categorical Groups (Policy_Type)
# Group the data
policy_types = data_final['Policy_Type'].unique()
premiums_by_policy = [data_final[data['Policy_Type'] == policy]['Premium_Amount'] for policy in policy_types]

# Perform ANOVA
f_stat, p_value = f_oneway(*premiums_by_policy)
print(f"F-statistic: {f_stat}, P-value: {p_value}")

"""**ANOVA for Categorical Groups (Policy_Type)**

Objective: Test if there’s a significant difference in premiums across different policy types.

Hypotheses:

- Null Hypothesis (H₀): There is no significant difference in premiums across policy types.

- Alternative Hypothesis (H₁): There is a significant difference in premiums across policy types.

**Interpretation:**

The p-value (0.0) is less than the common significance level of 0.05.

This means we reject the null hypothesis.

There is a statistically significant difference in premiums across different policy types.

*Action:
Including Policy_Type in my model, as it significantly impacts premiums.*
"""

# ANOVA for Region
# Group the data
regions = data_final['Region'].unique()
premiums_by_region = [data_final[data_final['Region'] == region]['Premium_Amount'] for region in regions]

# Perform ANOVA
f_stat, p_value = f_oneway(*premiums_by_region)
print(f"F-statistic: {f_stat}, P-value: {p_value}")

"""**ANOVA for Region**

*Hypothesis:*

Null Hypothesis (H₀): There is no significant difference in premiums across different regions.

Alternative Hypothesis (H₁): There is a significant difference in premiums across different regions.

**Interpretation:**

The p-value is extremely small (much less than 0.05), so we reject the null hypothesis.

This means there is a statistically significant difference in premiums across regions.

The large F-statistic indicates that the variation in premiums between regions is much larger than the variation within regions.

*Action:
Including Region in my model, as it significantly impacts premiums.*
"""

# T-Test for Binary Groups (Safe_Driver_Discount)
# Split data into two groups
safe_driver_premiums = data_final[data_final['Safe_Driver_Discount'] == 1]['Premium_Amount']
non_safe_driver_premiums = data_final[data_final['Safe_Driver_Discount'] == 0]['Premium_Amount']

# Perform t-test
t_stat, p_value = ttest_ind(safe_driver_premiums, non_safe_driver_premiums)
print(f"T-Statistic: {t_stat}, P-Value: {p_value}")

"""**T-Test for Binary Groups (Safe_Driver_Discount)**

Correlation with Target Varible: -0.13

Objective: Test if there’s a significant difference in premiums between safe drivers and non-safe drivers.

Hypotheses:

Null Hypothesis (H₀): There is no significant difference in premiums between safe drivers and non-safe drivers.

Alternative Hypothesis (H₁): There is a significant difference in premiums between safe drivers and non-safe drivers.

**Interpretation:**

The p-value is extremely small (much less than 0.05), so we reject the null hypothesis.

This means there is a statistically significant difference in premiums between safe drivers and non-safe drivers.

The negative T-statistic suggests that safe drivers tend to have lower premiums than non-safe drivers (or vice versa, depending on how the variable is encoded).

*Action:
Including Safe_Driver_Discount in my model makes sense, as it significantly impacts premiums.*
"""

# ANOVA for Source_of_Lead
source_of_lead_groups = [data[data['Source_of_Lead'] == source]['Premium_Amount'] for source in data['Source_of_Lead'].unique()]
f_stat, p_value = f_oneway(*source_of_lead_groups)
print(f"Source_of_Lead - F-statistic: {f_stat}, P-value: {p_value}")

# ANOVA for Conversion_Status
conversion_status_groups = [data[data['Conversion_Status'] == status]['Premium_Amount'] for status in data['Conversion_Status'].unique()]
f_stat, p_value = f_oneway(*conversion_status_groups)
print(f"Conversion_Status - F-statistic: {f_stat}, P-value: {p_value}")

"""**Interpretation:**

Source_of_Lead: Not relevant. I can exclude it from my model.

Conversion_Status: Relevant. Including it in my model and explore its relationship with Premium_Amount further.

# Feature Enginering
"""

# Dropping the unrelevant columns
data = data_final.drop(columns=['Source_of_Lead'])
# One-hot encode categorical columns in the entire dataset
# technique used to convert categorical variables into a format that can be provided to machine learning algorithms
categorical_cols = data.select_dtypes(include=['object', 'category']).columns
data_encode = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

# Check the new columns
print(data.columns)

# Define features (X) and target (y)
X = data_encode.drop('Premium_Amount', axis=1) # dropping the target variable from the rest of the features
y = data_encode['Premium_Amount'] # target variable

# Split the data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Check the shapes of the splits
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

"""**Interpretation:**

R² of 0.9886: Your model explains 98.86% of the variance in Premium_Amount, which is good. This suggests the model fits the data very well.

Low MSE: The model’s predictions are very close to the actual values, with minimal error

The **coefficient and feature importance analysis** needs to be conducted to understand the contribution of each feature to the model's predictions. By examining the coefficients in the linear regression model, we can identify which features have the most significant impact on the target variable (`Premium_Amount`). This helps in interpreting the model, validating that the relationships align with domain knowledge, and ensuring that no irrelevant or redundant features are influencing the results. Additionally, understanding feature importance aids in simplifying the model by highlighting key predictors, which can improve interpretability and potentially enhance performance by focusing on the most relevant variables.
"""

# Cross Validation Results (using k-fold)
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"Cross-Validation R² Scores: {cv_scores}")
print(f"Mean Cross-Validation R²: {cv_scores.mean()}")

"""Interpretation:
The high and consistent R² scores across all folds indicate that your model generalizes well to unseen data.

There’s no significant overfitting, as the performance is stable across different subsets of the data.

Conclusion:
Your model is robust and performs exceptionally well on both training and validation data.
"""

# Feature Importance
coefficients = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': model.coef_
})
print(coefficients.sort_values(by='Coefficient', ascending=False))

"""The coefficients from your linear regression model show the impact of each feature on Premium_Amount.

**Top Positive Contributors (Increase Premiums):**

- Region_Urban (100.54): Urban regions have the highest positive impact on premiums.

- Region_Suburban (50.49): Suburban regions also significantly increase premiums, though less than urban regions.

- Marital_Status_Widowed (2.25): Widowed individuals tend to have slightly higher premiums.

- Marital_Status_Single (1.11): Single individuals also have a small positive impact on premiums.

- Married_Premium_Discount (1.01): Being married slightly increases premiums (or reduces discounts).

**Top Negative Contributors (Decrease Premiums):**

- Total_Discounts (-1.00): More discounts significantly reduce premiums.

- Claims_Severity_Low (-0.84): Low claim severity reduces premiums.

- Conversion_Status (-0.75): Non-converted leads tend to have lower premiums.

- Credit_PCA (-0.70): Lower credit scores (or higher penalties) reduce premiums.

- Multi_Policy_Discount (-0.25): Having multiple policies reduces premiums.

**Neutral or Minimal Impact:**

- Age (0.007): Age has almost no impact on premiums.

- Time_to_Conversion (-0.003): Time to conversion has negligible impact.

- Policy_Type_Liability-Only (-0.005): Liability-only policies have a minimal negative impact.

# Ridge Regression

Ridge Regression is a regularized linear regression method that helps prevent overfitting by adding a penalty for large coefficients.

It’s useful when you have many features and want to ensure the model generalizes well to new data.

*Reason why I want to use it:*

- If my dataset has multicollinearity (even after PCA), Ridge Regression can handle it better than plain Linear Regression.

- It helps in stabilizing the model and reducing the variance of the coefficients.
"""

# Train Ridge Regression model
ridge_model = Ridge(alpha=1.0)  # alpha is the regularization strength
ridge_model.fit(X_train, y_train)

# Make predictions
y_pred_ridge = ridge_model.predict(X_test)

# Evaluate the model
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_ridge = r2_score(y_test, y_pred_ridge)

print(f"Ridge Regression Mean Squared Error: {mse_ridge}")
print(f"Ridge Regression R-squared: {r2_ridge}")

"""Ridge Regression performed very well, explaining 98.86% of the variance in Premium_Amount.

# KNN (K-nearest neigbors)

KNN is a non-parametric method that predicts the target variable based on the similarity of data points (neighbors).

It’s useful when the relationship between features and the target variable is non-linear.

*Reason why I used it:*

- It provides a different approach compared to linear models, as it doesn’t assume a linear relationship between features and the target.

- It can capture complex, non-linear patterns in the data that Linear Regression might miss..
"""

# Train KNN model
knn_model = KNeighborsRegressor(n_neighbors=5)  # Start with 5 neighbors
knn_model.fit(X_train, y_train)

# Make predictions
y_pred_knn = knn_model.predict(X_test)

# Evaluate the model
mse_knn = mean_squared_error(y_test, y_pred_knn)
r2_knn = r2_score(y_test, y_pred_knn)

print(f"KNN Mean Squared Error: {mse_knn}")
print(f"KNN R-squared: {r2_knn}")

"""KNN performed well but not as well as Ridge Regression, with 91.5% of the variance in premiums. This suggests that the relationship between features and premiums is more linear than non-linear.

Ridge Regression is the better model for my dataset, as it achieves higher accuracy and explains more of the variance in premiums.

KNN is a good alternative for exploring non-linear relationships, but in this case, it didn’t outperform Ridge Regression.

### **Next Steps in my Project**

**1. Advanced Machine Learning Models**

Why?: Linear models like Ridge Regression are great for now, but more complex models might capture additional patterns in the data.
Eg: random forest etc

**2. Hyperparameter Tuning for Ridge Regression**
Optimize the hyperparameters of the ML models to improve performance.

**3. Feature Engineering**

Why?: To improve or create new features that can enhance model performance.

**5. Final Model Selection**
Choose the best-performing model and prepare it for deployment.
"""