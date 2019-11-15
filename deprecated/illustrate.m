% Load data:
data = csvread('processed_data\calibration.csv', 1, 0);
I = data(:, 1);
O = data(:, 2);

% Plot with linear scale:
subplot(221)
plot(I, O)

% Plot with log scale on x axis:
subplot(222)
semilogx(I, O)

% Plot with log scale on y axis:
subplot(224)
semilogy(I, O)

% Plot with log scale on both axes:
subplot(223)
loglog(I, O)