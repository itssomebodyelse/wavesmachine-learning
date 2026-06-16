import copernicusmarine as cm
import xarray as xr
import pandas as pd

USERNAME = ""
PASSWORD = ""

print("Підключаємось до сервера...")

ds = cm.open_dataset(
    dataset_id="cmems_mod_blk_wav_my_2.5km_PT1H-i",
    username=USERNAME,
    password=PASSWORD
)

print("Вирізаємо координати та часовий проміжок...")

subset = ds.sel(
    time=slice("2023-01-01", "2024-01-01"),
    longitude=slice(29.0, 33.0),  
    latitude=slice(43.0, 46.5)    
)

print("Зменшуємо об'єм: беремо 1 запис на добу...")

daily_ds = subset.sel(time=subset.time.dt.hour == 12)
print("Формуємо таблицю...")

columns = ['VHM0', 'VTPK', 'VMDR']

df = daily_ds[columns].to_dataframe().reset_index().dropna()

output_csv = "black_sea_daily_waves.csv"
df.to_csv(output_csv, index=False)

print(f"Готово! Датасет збережено у {output_csv}. Кількість рядків: {len(df)}")
