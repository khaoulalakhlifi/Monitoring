from flask import Flask, render_template
import json
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('static.html')

@app.route('/fetchSystemInfo')
def fetch_system_info():
    try:
        # Read systemInfo.json
        with open('systemInfo.json', 'r') as file:
            data = json.load(file)

        # Create Matplotlib chart
        create_chart(data)

        return 'System information fetched and chart created successfully.'

    except Exception as e:
        return f'Error: {str(e)}'

def create_chart(data):
    labels = ['Memory Usage', 'CPU Usage', 'Disk Usage']
    values = [data['MemoryUsagePercent'], data['CpuUsagePercent'], data['DiskUsagePercent']]

    plt.bar(labels, values, color=['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)'],
            edgecolor=['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'], linewidth=1)

    plt.xlabel('System Info')
    plt.ylabel('Percentage')
    plt.title('System Information')
    plt.ylim(0, 100)  # Set the y-axis limit to 0-100

    # Save the plot to a file or use plt.show() to display in the console
    plt.savefig('static/system_chart.png')

if __name__ == '__main__':
    app.run(debug=True)
