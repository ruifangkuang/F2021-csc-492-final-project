import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.offline as plt

from models import ProgressRecord


def format_progress_data_df(user, db):

    records = ProgressRecord.query.filter_by(user_id=user.id)
    
    pre_df_dict ={
        'date_taken':[],
        'stress_rating':[],
        'positive_thinking_rating':[],
        'recognize_stigma_rating':[],
        'problem_solving_rating':[]
    }
    for record in records:
        pre_df_dict['date_taken'].append(record.date_taken)
        pre_df_dict['stress_rating'].append(record.stress_rating)
        pre_df_dict['positive_thinking_rating'].append(record.positive_thinking_rating)
        pre_df_dict['recognize_stigma_rating'].append(record.recognize_stigma_rating)
        pre_df_dict['problem_solving_rating'].append(record.problem_solving_rating)

    data_df = pd.DataFrame.from_dict(pre_df_dict)

    return data_df

def create_progress_chart(user, db):
    data_df = format_progress_data_df(user, db)

    fig = go.Figure()

    # Add trace for each metric type.
    for column in data_df.columns[1:]:
        fig.add_trace(go.Scatter(x=data_df['date_taken'], y=data_df[column],
                            mode='lines',
                            name=f"{column.replace('_', ' ').capitalize()}"))
                            
    fig.update_layout(title=f"How are you progressing over time?")
        
    time_series = plt.plot(fig, output_type='div', config={'displaylogo': False})
    

    return time_series