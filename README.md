ABSTRACT

This project aims to predict auto insurance premiums using a synthetic dataset designed to mirror real-world insurance data. The dataset includes customer attributes such as age, marital status, prior insurance history, claims frequency, and more. By leveraging machine learning techniques, including linear regression and ensemble methods like random forest and gradient boosting, we seek to build a model that accurately forecasts insurance premium amounts. The project not only highlights the impact of customer-specific factors on pricing but also demonstrates how machine learning can be applied in the insurance industry for risk assessment and premium optimization. The use of this synthetic dataset allows for realistic yet secure experimentation, providing valuable insights without compromising privacy.

Data Link:

https://www.kaggle.com/datasets/samialyasin/insurance-data-personal-auto-line-of-business?resource=download

 Methodology

1. Data Collection and Preprocessing:
   - Found a dataset containing customer demographics, policy details, claims history, and premium amounts.  
   - Handled missing values, encoded categorical variables, and standardized numerical features.  

3. Exploratory Data Analysis (EDA):  
   - Analyzed feature distributions, correlations, and relationships with the target variable (`Premium_Amount`).  
   - Conducted hypothesis testing (e.g., t-tests, ANOVA) to identify significant differences in premiums across groups (e.g., `Region`, `Policy_Type`).  

4. Addressing Multicollinearity:  
   - Identified highly correlated features (e.g., `Claims_Frequency` and `Claims_Adjustment`) using a correlation matrix.  
   - Applied Principal Component Analysis (PCA) to create composite features (`Claims_PCA`, `Credit_PCA`) and reduce redundancy.  

5. Model Development:  
   - Split the data into training (80%) and testing (20%) sets.  
   - Built and evaluated multiple models:  
     - Linear Regression: Baseline model for understanding linear relationships.  
     - Ridge Regression: Regularized model to handle multicollinearity and prevent overfitting.  
     - K-Nearest Neighbors (KNN): Non-parametric model to explore non-linear relationships.  

6. Model Evaluation:  
   - Evaluated models using Mean Squared Error (MSE) and R-squared (R²) to assess accuracy and variance explained.  
   - Compared performance across models to identify the best-performing one.  

7. Insights and Next Steps:  
   - Identified key drivers of premiums (e.g., `Policy_Adjustment`, `Claims_PCA`, `Credit_PCA`).  
   - Outlined next steps, including hyperparameter tuning, advanced modeling (e.g., Random Forest, XGBoost), and feature engineering.  
