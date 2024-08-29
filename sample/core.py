def growth_curve_analysis(time, od, title, threshold = 30, show_derivitive = False):
  # Calculate the derivative of the OD values
  window = 1
  derivitive = np.diff(od, n=window)/np.diff(time,n=window)
  smoothed_derivative = gaussian_filter1d(derivitive, sigma=2)

  if show_derivitive:
    plt.plot(time[1:], smoothed_derivative)
    plt.show()

  threshold = threshold  # Adjust this based on your data

  log_phase_x = time[1:][smoothed_derivative > threshold]
  log_phase_y = od[1:][smoothed_derivative > threshold]

  plt.figure(figsize=(10, 6))
  plt.plot(time, od, label=title, marker='o', markersize=1)
  plt.plot(log_phase_x, log_phase_y, label='Log phase', marker='o', markersize=1)

  # Step 4: Perform linear regression on the identified exponential phase
  slope, intercept, r_value, p_value, std_err = linregress(log_phase_x, log_phase_y)
  # print()


  lag_time = 0
  line_lower_bound = 0
  line_upper_bound = 0

  for index, i in enumerate((intercept + slope*time)):
    if i > np.min(od) and line_lower_bound == 0:
      line_lower_bound = index - 1
      lag_time = time.iloc[index]
    if i > np.max(od) and line_upper_bound == 0:
      line_upper_bound = index + 1
      # print(lag_time)
      break

  plt.plot(time[line_lower_bound:line_upper_bound], intercept + slope*time[line_lower_bound:line_upper_bound], 'r', label='fitted line')

  plt.axhline(y=np.min(od), color='green', linestyle='--', label=f'Baseline')
  plt.axhline(y=np.max(od), color='blue', linestyle='--', label=f'Max')

  plt.axvline(x=lag_time, color='red', linestyle='--', label=f'Lag Time')


  plt.xlabel('Time(h)')
  plt.ylabel('OD Gain 2')
  plt.title(title)

  plt.legend()

  plt.figtext(0.5, 0.5, f'Growth rate: {slope:.2f}' + f'\nLag Time: {lag_time:.2f}' + f'\nMax Biomass: {np.max(od):.2f}')

  plt.show()
  pass