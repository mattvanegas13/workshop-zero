Realized Volatility Walk-Forward Experiment Spec

Research Question

Does knowing recent realized volatility help us predict subsequent volatility?

Feature

For each day (t), define the 20-day realized-variance proxy as:

[
X_t = RV_{20,t} = \frac{1}{20}\sum_{i=t-19}^{t} r_i^2
]

Because the prediction is assumed to be made after market close on day (t), the return from day (t) is available and can be included.

Target

The actual next-day volatility proxy is:

[
y_t = r_{t+1}^2
]

The model produces a prediction:

[
\hat{y}_t
]

Model

Start with a simple linear regression:

[
y_t = \beta_0 + \beta_1 X_t + \epsilon_t
]

The purpose is to test the hypothesis with the simplest model capable of doing so. More complex features or models can be introduced later as separate experiments.

Validation Scheme

Use expanding walk-forward validation with one-year test periods.

Example:

[
2020\text{–}2021 \rightarrow 2022
]

[
2020\text{–}2022 \rightarrow 2023
]

[
2020\text{–}2023 \rightarrow 2024
]

[
2020\text{–}2024 \rightarrow 2025
]

For each fold, all learned quantities must be estimated using the training data only.

This includes:

Regression coefficients

Scaler mean and standard deviation, if standardization is used

Baseline statistics

Baseline

Under squared-error loss, the best constant prediction is the expected value of (Y).

Because the true (E[Y]) is unknown, estimate it using the training-set mean:

[
\hat{E}[Y] = \bar{y}_{\text{train}}
]

The baseline therefore predicts the same constant value for every observation in the test period:

[
\hat{y}t^{\text{baseline}} = \bar{y}{\text{train}}
]

Evaluation

For the model:

\frac{1}{N}
\sum_{t \in \text{test}}
(\hat{y}_t - y_t)^2
]

For the baseline:

\frac{1}{N}
\sum_{t \in \text{test}}
(\bar{y}_{\text{train}} - y_t)^2
]

Then compare:

[
MSE_{\text{model}} < MSE_{\text{baseline}}
]

If the model using (X_t) repeatedly achieves lower out-of-sample MSE than the training-mean baseline, that is evidence that (X_t) contains useful predictive information about (y_t).

Further testing is needed to determine whether the relationship is statistically robust, stable across folds, and economically meaningful.

Core Interpretation

Without (X_t), the best constant guess under MSE loss is approximately:

[
E[Y]
]

With (X_t), the model attempts to approximate:

[
E[Y \mid X_t]
]

The core experiment asks whether knowing (X_t) improves prediction enough to outperform the unconditional baseline.
