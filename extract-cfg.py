import re 
output = """
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1031.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1051.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1121.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1141.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1171.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg11.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1211.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1231.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1251.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1261.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg1311.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg131.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1351.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1371.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1431.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1471.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1481.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg151.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1521.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1541.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1561.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1591.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg161.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1621.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1651.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1661.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1671.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1691.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1751.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1781.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1791.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg1801.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1811.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg181.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1821.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1861.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1901.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg1921.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg201.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg211.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg231.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg261.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg291.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg301.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg341.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg371.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:20 peram_32_cfg41.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg421.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg461.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg471.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg501.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg511.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg531.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:27 peram_32_cfg551.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg581.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg591.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:25 peram_32_cfg61.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg631.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:26 peram_32_cfg661.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:28 peram_32_cfg701.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 15:25 peram_32_cfg71.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 22:05 peram_32_cfg751.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 22:10 peram_32_cfg801.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  1 22:25 peram_32_cfg811.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  2 00:41 peram_32_cfg901.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  2 00:40 peram_32_cfg91.sdb
-rw-rw-r-- 1 bradley1 exotichadrons    0 Sep  2 00:47 peram_32_cfg971.sdb"""
cfg_numbers = re.findall(r'cfg(\d+)\.sdb', output)

# Convert the matches to integers (optional)
cfg_numbers = [f'"{num}"' for num in cfg_numbers]

print(cfg_numbers)