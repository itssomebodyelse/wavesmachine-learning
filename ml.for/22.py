import xarray as xr
import pandas as pd

# Шлях до вашого завантаженого файлу
file_path = 'cmems_mod_blk_wav_my_2.5km_PT1H-i_1777798275803.nc'

# Відкриваємо NetCDF файл
ds = xr.open_dataset(file_path)

# Перетворюємо багатовимірний масив у плоский pandas DataFrame
df = ds.to_dataframe().reset_index()

# Фільтруємо лише потрібні колонки (час, координати, висота, період, напрям)
# Назви колонок можуть трохи відрізнятися залежно від обраних змінних при завантаженні
columns_to_keep = ['time', 'latitude', 'longitude', 'VHM0', 'VTPK', 'VMDR']
df_filtered = df[columns_to_keep].dropna()

# Зберігаємо готовий датасет у CSV
output_csv = 'black_sea_waves_dataset.csv'
df_filtered.to_csv(output_csv, index=False)

print(f"Датасет успішно збережено у {output_csv}. Кількість записів: {len(df_filtered)}")