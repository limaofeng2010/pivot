import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    a_df = pd.read_xml('../Data/A_office_data.xml')
    b_df = pd.read_xml('../Data/B_office_data.xml')
    hr_df = pd.read_xml('../Data/hr_data.xml')

    a_ids = a_df['employee_office_id'].values
    b_ids = b_df['employee_office_id'].values
    a_new_ids = []
    b_new_ids = []

    a_df['employee_id'] = 'A' + a_df['employee_office_id'].astype(str)
    a_df.set_index('employee_id', inplace=True)
    # print(a_df['employee_office_id'].dtypes)
    # print(a_df.info)

    b_df['employee_id'] = 'B' + b_df['employee_office_id'].astype(str)
    b_df.set_index('employee_id', inplace=True)
    # print(b_df.info)

    ab_df = pd.concat([a_df, b_df])
    # ab_df.drop([''])
    # print(ab_df)

    hr_df.set_index('employee_id', inplace=True)
    # print(hr_df)

    hr_df = ab_df.join(hr_df, how='left')
    hr_df.drop(columns=['employee_office_id'], inplace=True)
    hr_df.dropna(inplace=True)
    # print(hr_df.info)
    # print(hr_df.axes[1])
    hr_df = hr_df.sort_index()
    # print(list(map(lambda x: int(x), hr_df['left'].to_list())))
    hr_df['left'] = hr_df['left'].astype(int)
    # print(hr_df.dtypes)
    # print(hr_df)

    # print(list(hr_df.index))
    # print(list(hr_df.columns))
    # print(hr_df)

    # print(hr_df.sort_values('average_monthly_hours', ascending=False).head(10)['Department'].to_list())
    # print(hr_df[(hr_df.Department=='IT') & (hr_df.salary=='low')]['number_project'].sum())
    # print(hr_df.loc[['A4', 'B7064', 'A3033']][['last_evaluation','satisfaction_level']].values.tolist())

    # define the function which filter the employee who worked on more than five projects
    # def count_bigger_5(series):
    #     return series.where(series > 5).count()
    #
    # result_df = hr_df.groupby(['left']).agg({
    #     'number_project': ['median', count_bigger_5],
    #     'time_spend_company': ['mean', 'median'],
    #     'Work_accident': 'mean',
    #     'last_evaluation': ['mean', 'std']
    # })

    av_hours_df = hr_df.pivot_table(index='Department',
                            columns=['left', 'salary'], values='average_monthly_hours', aggfunc='median').round(2)

    # print(av_hours_df)
    result1_df = av_hours_df.loc[((av_hours_df[0, 'high'] < av_hours_df[0, 'medium']) | (av_hours_df[1, 'low'] < av_hours_df[1, 'high']))]
    # print(result1_df)
    print(result1_df.to_dict())

    time_df = hr_df.pivot_table(index='time_spend_company',
                                columns='promotion_last_5years',
                                values=['satisfaction_level','last_evaluation'],
                                aggfunc=['mean', 'min', 'max']).round(2)
    # print(time_df)

    # print(time_df.loc[time_df['mean', 'last_evaluation', 1] > time_df['mean', 'last_evaluation', 0]])
    print(time_df.loc[time_df['mean', 'last_evaluation', 1] < time_df['mean', 'last_evaluation', 0]].to_dict())

