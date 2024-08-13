import numpy as np
import matplotlib.pyplot as plt

def parse_pppnava_line(line):
    parts = line.strip().split(',')
    latitude = float(parts[11])
    longitude = float(parts[12])
    altitude = float(parts[13])
    return latitude, longitude, altitude

def compute_rms(values):
    mean_value = np.mean(values)
    rms_value = np.sqrt(np.mean((values - mean_value) ** 2))
    return rms_value

def lat_lon_to_meters(lat_diff, lon_diff, latitude):
    # 地球半径（米）
    earth_radius = 6378137.0
    # 将纬度差转换为米
    lat_diff_meters = lat_diff * (np.pi / 180) * earth_radius
    # 将经度差转换为米
    lon_diff_meters = lon_diff * (np.pi / 180) * earth_radius * np.cos(np.deg2rad(latitude))
    return lat_diff_meters, lon_diff_meters

def read_and_analyze_pppnava_file(filename):
    latitudes = []
    longitudes = []
    altitudes = []

    # 读取文件并解析PPPNAVA报文
    with open(filename, 'r') as file:
        for line in file:
            latitude, longitude, altitude = parse_pppnava_line(line)
            latitudes.append(latitude)
            longitudes.append(longitude)
            altitudes.append(altitude)

    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    altitudes = np.array(altitudes)

    # 计算经纬度和高度的平均值和RMS值
    mean_latitude = np.mean(latitudes)
    mean_longitude = np.mean(longitudes)
    mean_altitude = np.mean(altitudes)

    rms_latitude = compute_rms(latitudes)
    rms_longitude = compute_rms(longitudes)
    rms_altitude = compute_rms(altitudes)

    print(f"RMS Latitude: {rms_latitude:.10f}°")
    print(f"RMS Longitude: {rms_longitude:.10f}°")
    print(f"RMS Altitude: {rms_altitude:.10f} m")

    # 经纬度差异转换为米
    latitude_diff = latitudes - mean_latitude
    longitude_diff = longitudes - mean_longitude
    lat_diff_meters, lon_diff_meters = lat_lon_to_meters(latitude_diff, longitude_diff, mean_latitude)

    # 可视化
    plt.figure(figsize=(12, 18))

    # 经纬度散点图，标注平均值
    plt.subplot(3, 1, 1)
    plt.scatter(longitudes, latitudes, color='blue', label='Positions')
    plt.scatter(mean_longitude, mean_latitude, color='red', label='Mean Position', marker='x', s=100)
    plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%.10f'))
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.10f'))
    plt.title("Position Plot with Mean Position")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)

    # 高度变化图
    plt.subplot(3, 1, 2)
    plt.plot(altitudes, color='green', label='Altitude')
    plt.axhline(mean_altitude, color='red', linestyle='--', label='Mean Altitude')
    plt.title(f"Altitude Plot (RMS: {rms_altitude:.10f} m)")
    plt.xlabel("Sample Index")
    plt.ylabel("Altitude (m)")
    plt.legend()
    plt.grid(True)

    # 经纬度与平均值差异（米）
    plt.subplot(3, 1, 3)
    plt.plot(lat_diff_meters, label='Latitude Difference (m)', marker='o')
    plt.plot(lon_diff_meters, label='Longitude Difference (m)', marker='o')
    plt.title("Latitude and Longitude Difference from Mean (Meters)")
    plt.xlabel("Sample Index")
    plt.ylabel("Difference (m)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# 示例：读取并分析存储PPPNAVA报文的txt文件
read_and_analyze_pppnava_file('PPPNAVA_8_9-15-56.txt')
