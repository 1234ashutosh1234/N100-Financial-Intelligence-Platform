from src.dashboard.utils.db import *

print(get_companies().head())
print(get_ratios().head())
print(get_rankings().head())
print(get_peer_percentiles().head())