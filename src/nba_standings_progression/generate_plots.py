from pathlib import Path
import standings_progression as sp


DATA_DIR = Path('./standings_data')
OUTPUT_DIR = Path('./plots')
DATA_FILE_PATTERN = '*.xlsx'
IMG_FORMAT = '.png'

data_files = sorted(DATA_DIR.glob(DATA_FILE_PATTERN))

for file in data_files:

  try:
    ws_data = sp.get_standings_data_from_spreadsheet(str(file))
  except:
    print("Something went wrong with " + str(file))
    continue

  win_frac_data = sp.process_standings_data(ws_data)
  fig = sp.plot_standings_progression(win_frac_data)
  out_file = OUTPUT_DIR / file.with_suffix(IMG_FORMAT).name
  fig.savefig(str(out_file), format=IMG_FORMAT[1:])
