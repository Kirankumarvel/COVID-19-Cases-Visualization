import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib import rcParams

def create_covid_dashboard():
    # Create directories if they don't exist
    os.makedirs('assets', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # Load data
    try:
        df = pd.read_csv('data/covid_data.csv', parse_dates=['date'])
    except FileNotFoundError:
        print("Error: data/covid_data.csv not found. Using sample data.")
        df = pd.DataFrame({
            'date': pd.date_range(start='2023-01-01', periods=7),
            'cases': [150, 180, 210, 190, 220, 250, 230],
            'deaths': [5, 7, 8, 6, 9, 12, 10],
            'recoveries': [120, 135, 160, 155, 180, 210, 195]
        })

    # Set style
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
    plt.style.use('ggplot')

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('COVID-19 Cases Analysis', fontsize=16, fontweight='bold', y=1.02)

    # Line Chart - Daily Cases
    ax1.plot(df['date'], df['cases'], 
             marker='o', 
             color='#1f77b4', 
             linewidth=2.5,
             label='Daily Cases')
    ax1.set_title('Daily COVID-19 Cases', pad=20)
    ax1.set_ylabel('Number of Cases')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    # Bar Chart - Deaths vs Recoveries
    width = 0.35
    x = range(len(df['date']))
    ax2.bar([i - width/2 for i in x], df['deaths'], 
            width, 
            color='#d62728', 
            label='Deaths')
    ax2.bar([i + width/2 for i in x], df['recoveries'], 
            width, 
            color='#2ca02c', 
            label='Recoveries')
    ax2.set_title('Deaths vs Recoveries', pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df['date'].dt.strftime('%m-%d'))
    ax2.set_ylabel('Count')
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--', alpha=0.6)

    # Highlight peak values
    max_cases = df.loc[df['cases'].idxmax()]
    ax1.annotate(f'Peak: {max_cases["cases"]} cases',
                xy=(max_cases['date'], max_cases['cases']),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                arrowprops=dict(arrowstyle='->'))

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('assets/covid_dashboard.png', dpi=120, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    create_covid_dashboard()