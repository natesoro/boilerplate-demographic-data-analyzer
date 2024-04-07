import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("/workspace/boilerplate-demographic-data-analyzer/adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series(df['race']).value_counts()

    # What is the average age of men?
    #average_age_men = df.groupby('sex').mean()['age']['Male'] //deprecated approach
    df_all_male = df.query('sex == "Male"')
    average_age_men = (df_all_male['age'].sum() / len(df_all_male)).round(1)

    # What is the percentage of people who have a Bachelor's degree?
    s_education = pd.Series(df['education'])
    percentage_bachelors = round((s_education.value_counts()['Bachelors'] / s_education.value_counts().sum()) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    df_higher_educ = df.query('education == "Bachelors" | education =="Masters" | education == "Doctorate"')
    df_higher_educ_greater50k = df_higher_educ.query('salary == ">50K"')
    higher_education_rich = round((df_higher_educ_greater50k.shape[0] / df_higher_educ.shape[0]) * 100, 1)

    # percentage with salary >50K
    df_lower_educ = df.query('education != "Bachelors" & education != "Masters" & education != "Doctorate"')
    df_lower_educ_greater50k = df_lower_educ.query('salary == ">50K"')
    lower_education_rich = round((df_lower_educ_greater50k.shape[0] / df_lower_educ.shape[0]) * 100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    df_min_hours_workers = df.query('`hours-per-week` == 1')
    df_rich = df_min_hours_workers.query('salary == ">50K"')
    rich_percentage = round((df_rich.shape[0] / df_min_hours_workers.shape[0]) * 100,1)

    # What country has the highest percentage of people that earn >50K?
    df_highest_earning = pd.concat([df.query('salary==">50K"').groupby(['native-country']).size(), df.groupby(['native-country']).size()], axis=1, join="inner")
    #20240407 Niño: removed redundant and unused variable
    #df_percentage_highest_earning = df_highest_earning['percentage'] = (df_highest_earning[0] / df_highest_earning[1]) * 100
    df_highest_earning['percentage'] = (df_highest_earning[0] / df_highest_earning[1]) * 100
    #//
    highest_earning_country = (df_highest_earning).loc[df_highest_earning['percentage'].idxmax()].name
    highest_earning_country_percentage = (df_highest_earning).loc[df_highest_earning['percentage'].idxmax()]['percentage'].round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = (df.query('`native-country` == "India" & salary == ">50K"').groupby(['occupation']).size()).idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
