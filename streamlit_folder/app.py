import streamlit as st
import pandas as pd
import sys
import os
import pickle
from io import StringIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# 'streamlit_folder' 폴더의 실제 경로를 계산합니다.
#open(r'C:\Users\user\OneDrive\바탕 화면\AI_Outsourcing\streamlit_folder\custom.css')
#open('C:\Users\user\OneDrive\바탕 화면\AI_Outsourcing\streamlit_folder\custom.css')
#css_content = file.read()
#with open('custom.css', 'r', encoding='utf-8') as file:
#    custom_css = file.read()

#st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)


def get_row_color(prediction):
    if prediction == 0: 
        return 'background-color: green;'
    elif prediction == 1:
        return 'background-color: yellow;'
    elif prediction == 2:
        return 'background-color: orange;'
    elif prediction == 3:
        return 'background-color: red;'
    
def assign_label(task):
    if task == 'PM':
        return 1
    elif task =='백엔드 개발자':
       return 2
    elif task == '프론트엔드 개발자':
       return 3
    elif task == 'DB 관리자':
       return 4
    else:
       return 5
    
 # 표 생성
table_html = f"""
    <table style="width: 100%;">
        <tr>
            <td style="background-color: #FFDBD9; text-align: center; border: none; border-radius: 8px 0 0 8px; font-weight: bold; color: black;">0</td>
            <td style="background-color: #FFB6B2; text-align: center; border: none; font-weight: bold; color : black; ">1</td>
            <td style="background-color: #F0867D; text-align: center; border: none; font-weight: bold; color : black; ">2</td>
            <td style="background-color: #EC5147; text-align: center; border: none; border-radius : 0 8px 8px 0; font-weight: bold; color:black;">3</td>
        </tr>
    </table>
    """#


st.markdown("""
    <style>
        body {
            background-color: #000000;
            max-width : 100%
        }       
            
        .title {
            font-family: Verdana, sans-serif; /* Verdana 폰트를 사용 */
            font-size: 24px; /* 원하는 글꼴 크기 설정 */
            color: blue; /* 글꼴 색상 설정 */
        }   
                    
        table {
            border-collapse: collacpse;
            width: 50%;
            color : white;
        }

        th, td {
            text-align: center;
            padding: 9px;
            }
        </style>
""", unsafe_allow_html=True)


st.title('GUESS WHO') 

streamlit_folder_path = os.path.abspath(os.path.join('../../AI_Outsourcing', 'streamlit_folder'))

# 'streamlit_folder' 폴더의 경로를 Python 경로에 추가합니다.
if streamlit_folder_path not in sys.path:
    sys.path.append(streamlit_folder_path)

# 'predict.py' 파일에서 함수를 가져옵니다.
from predict import predict_model
# 파일 업로드 기능
uploaded_file = st.file_uploader('file upload', type=['csv'])

def main():
    
    with open('model.pkl', 'rb') as f: 
        model = pickle.load(f) 
    print("-------------------")
    print(model) 
    
    colors = {0: '#FFDBD9', 1: '#FFB6B2', 2: '#F0867D', 3: '#EC5147'}

    if uploaded_file is not None:
    # 업로드된 파일을 데이터프레임으로 읽기
        data= uploaded_file.read().decode('euc-kr')
        data2 = pd.read_csv(StringIO(data))
    # 데이터셋 확인
        st.subheader('미리보기')
        st.dataframe(data2)
        
        # 위험도 분석 버튼
        if st.button('공격 위험도 예측 시작'):
    # 예측 결과 가져오기
            data3=data2.copy()
            data2['담당업무'] = data2['담당업무'].apply(assign_label)
            data2.drop(columns='사용자 ID', inplace=True)
        
            test = model.predict(data2)
            test_value=test.copy()

            new=pd.DataFrame()
            new['사용자 ID']=data3['사용자 ID']
            new['공격 위험도']=test
            new['사용자 ID']=new['사용자 ID'].astype(str)
            new['공격 위험도']=new['공격 위험도'].astype(str)
            #str1='  '*5
            #new['공격 위험도']=str1 + new['공격 위험도']
            new1=new.set_index(['사용자 ID','공격 위험도'])
            a=new1.copy()
            new['공격 위험도']=new['공격 위험도'].astype(str)          
            new2=new.set_index('사용자 ID')
            new_setting=new2.copy()
            #new_setting


            def style_table(data):
                 styled_table = data.style.set_properties(**{
                     'text-align': 'center',
                     'color': 'white'
                 })
                 styled_table = styled_table.set_table_styles([{
                     'selector': 'th',
                     'props': [('color', 'white')]
                 }])
                 return styled_table

            #styled_data = style_table(new_setting)
            #styled_data.index.name = '사용자 ID'
            styler=a.style
            styler.set_properties(**{'text-align': 'center'})
            styler.set_table_styles([
                {'selector': 'th', 'props': 'text-align: center;'},
                {'selector': 'td', 'props': 'text-align: center;'},         
            ])
            styler = styler.set_caption('사용자별 공격 위험도')  # 표 제목 설정

            # Styler를 HTML로 변환하여 표시ㄴ
            html_table = styler.to_html(escape=False).replace('<table', '<table style="width: 100%;"')

            # HTML을 Streamlit에 표시
            st.write(html_table, unsafe_allow_html=True)
            #st.table(new_setting)


           
            # styles = [dict(selector="th", props=[("text-align", "center"), ("color", "white")]),
            #            dict(selector="td", props=[("text-align", "center"), ("color", "white")])
            # ]
            # styled_data = new_setting.style.set_table_styles(styles)
            # styled_data = styled_data.set_table_attributes('border="1" class="dataframe"')
            # styled_data.index.name = '사용자 ID'
            # styled_data
        
            # styled_new = new_setting.style
            # styled_new = style_table(styled_new)
            
            # st.table(styled_new)
        
        # 그래프를 Streamlit에 표시
            #st.pyplot(fig)
            # new_setting=new.copy()
            # styles = [dict(selector = "thead th", 
            #    props = [("font-size", "150%"), ("text-align", "center")]),
            #    dict(selector="td", props= [("font-size", "150%"), ("text-align", "center")])]
            # new.style.set_table_styles(styles)
            # new
            # #st.write(test)
            # # print(test)  
            # # prediction을 list화 하기
            # st.markdown("""
            #     <div style="float: left; width: 100%;">
            #         <h2>그래프</h2>
            #     </div>
            # """, unsafe_allow_html=True)

            # # 그래프 생성
            # fig, ax = plt.subplots()
            # colors = ['#FFDBD9', '#FFB6B2', '#F0867D', '#EC5147']
            # ax.pie(
            #     [data.count(value) for value in set(data)],
            #     labels=[f'{value}: {data.count(value)}' for value in set(data)],
            #     autopct='',
            #     colors=colors,
            #     startangle=90,
            #     counterclock=False,
            #     wedgeprops={'width': 0.4}
            # )
            # ax.set(aspect="equal")
            # fig.set_facecolor('none')

            #st.subheader("공격 위험도별 비율")
            #st.pyplot(fig)

            # 공격 위험도 값에 따라 사용자 ID 그룹화
          # 테이블 생성
           
            # st.markdown("""
            #     <div style="float: right; width: 50%;">
            #         <h2>데이터프레임</h2>
            #     </div>
            # """, unsafe_allow_html=True) 
            # def apply_style(row):
            #     background_color_mapping = {
            #         "매우 위험한 단계입니다\n 자동으로 로그인 차단을 실행합니다.": 'background-color: #FF3333;',
            #         "주의 단계입니다\n 자동으로 일부 기능 차단을 실행합니다.": 'background-color: #FF6666;',
            #         "경계 단계입니다\n 지속적인 경계가 필요합니다.": 'background-color: #FF9999;',
            #         "정상입니다." : 'background-color: #FFE5E5;',
            #     }
            #     return [background_color_mapping.get(row['memo'], '') for _ in row]

            # styled_last = last.style.apply(apply_style, axis=1)
            # styled_last.set_properties(**{'color': '', 'border-color': 'black'})
            # styled_last.set_table_styles([{'selector': 'th', 'props': [('color', 'black')]}])
            # st.table(styled_last)
            # st.markdown("<style>table td {color: black;}</style>", unsafe_allow_html=True)
            
            # st.write(styled_last)

            # 페이지를 두 개의 열로 나누어 그래프와 데이터프레임을 배치
            #col1, col2 = st.columns(2)
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("")
                st.markdown("")
                st.markdown("")
                st.markdown("  <h4>사용자 분포</h4>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                data_counts = [new_setting['공격 위험도'].value_counts().get(i, 0) for i in range(4)]
                labels = [f'{i}: {count}' for i, count in enumerate(data_counts)]

                ax.pie(data_counts, labels=[""]*4, autopct='', colors=[colors[i] for i in range(4)], startangle=90, counterclock=False, wedgeprops={'width': 0.4})
                ax.set(aspect="equal")
                fig.set_facecolor('none')
                st.pyplot(fig)


                st.markdown(table_html, unsafe_allow_html=True)
                
                
                # new=pd.DataFrame()
                # new['사용자 ID']=data3['사용자 ID']
                # new['공격 위험도']=test
                # new=new.set_index('사용자 ID')
                # new_setting=new.copy()
                # #st.table(new_setting)   
                # #styles = [dict(selector = "thead th", 
                # #props = [("font-size", "150%"), ("text-align", "center")]),
                # #dict(selector="td", props= [("font-size", "150%"), ("text-align", "center")])]
                # #new.style.set_table_styles(styles).set_properties(**{'width':'100%'})
                # styles = [
                #     dict(selector="th", props=[("text-align", "center"),("color", "white")]),
                #     dict(selector="td", props=[("text-align", "center"),("color", "white")])
                # ]
                # #st.table(new_setting.style.set_table_styles(styles).hide_index())
                # #new.reset_index(inplace=Tr ue)
                # #st.table(new_setting.reset_index(drop=True).style.set_table_styles(styles))
                # #st.table(new_setting.rename_axis(index=None).style.set_table.styles)
                # #st.table(new_setting.style.hide_index())
                # #styled_new = new_setting.style.set_table_styles(styles)
                # def style_table(data3, test, fig):
                # # 코드 내용...
                #     styles = [
                #         dict(selector="th", props=[("text-align", "center"), ("color", "white")]),
                #         dict(selector="td", props=[("text-align", "center"), ("color", "white")]),
                #     ]
                #     # styled_new = new_setting.style.set_table_styles(styles)
                #     # styled_new.index.name = '사용자 ID'
                #     # styled_new = styled_new.set_table_attributes('border="1" class="dataframe"')
                #     # return styled_new
                
                # st.table(style_table(data3, test, fig))
                
                #styled_new = styled_new.set_caption('사용자 ID').set_table_attributes('style="text-align: center; color: white;"')
                #styled_new = style_table(data3, test, fig)
                #st.table(styled_new)
            with col2:
                st.markdown("")
                st.markdown("")
                st.markdown("")
                st.markdown("  <h4>위험도 분류</h4>", unsafe_allow_html=True)
                new_setting=new_setting.reset_index()
                
                a=new_setting.copy()
                a=a.rename(columns={'사용자 ID': '　', '공격 위험도': '　　','memo':'　　　'})
                a['　']=a['　'].astype(str)
                a=a.groupby('　　').sum().reset_index()
                #a.index=a.index.astype(str, allow_duplicates=True)
                a['　']=a['　'].str.replace(r'(\d{4})(?=\d)', r'\1,', regex=True)
                a['　　　']=' '
            
            
            
                for i, row in a.iterrows():
                    if i == 3:
                        a.at[i, '　　　'] = "해당 사용자의 계정에 대한"+"　　　　　" +"자동 로그인이 차단되었습니다."+"　　　　　　　　"+"해당 사용자와의 연락을 즉시 시도하여 활동을 확인하세요."
                    elif i == 2:
                        a.at[i, '　　　'] = "해당 사용자의 활동을 검토하여"+"　　　　　　　　　　"+"어떤 위협이나 취약성이 있는지"+"　　　"+ "확인이 필요합니다."
                    elif i == 1:
                        a.at[i, '　　　'] = " 해당 사용자에 대한 지속적인"+"　　　　"+"주의 관리가 필요합니다. "
                    elif i == 0:
                        a.at[i, '　　　'] = "특별한 대응 조치가 필요하지 않습니다."
            
                #last = new_setting.set_index('공격 위험도')

                 #last = new_setting.set_index('공격 위험도')
                last=a
                                # styler=last.style.format()
                # st.write(styler.to_html(), unsafe_allow_html=True)
                #last_no_index = last.reset_index(drop=True)
                #st.table(last_no_index)

                #st.table(last_without_index)\
                #def apply_style(row):
                        # "매우 위험한 단계입니다.\n 자동으로 로그인 차단을 실행합니다.": 'background-color: #EC5147;',
                        # "주의 단계입니다.\n 자동으로 일부 기능 차단을 실행합니다.": 'background-color: #F0867D;',
                        # "경계 단계입니다.\n 지속적인 경계가 필요합니다.": 'background-color: #FFB6B2;',
                        # "정상입니다." : 'background-color: #FFDBD9;',
                colors = {
                        '0': 'background-color: #FFDBD9; color: black;',
                        '1': 'background-color: #FFB6B2; color: black;',
                        '2': 'background-color: #F0867D; color: black;',
                        '3': 'background-color: #EC5147; color: black;'
                    }
                #return [color_mapping.get(row, '') for row in test]
                    #return [background_color_mapping.get(row['memo'], '') for row in test]
                
                styler=last.style
                styler = styler.apply(lambda row: [colors.get(row['　　'], '')]*len(row), axis=1)
                st.table(styler)
                #st.dataframe(styler, use_container_width=True, header=False)
                # last=new_setting,
                # styler=last.style
                # def apply_style(row):
                #     colors = {
                #         0: 'background-color: #FFDBD9; color: black;',
                #         1: 'background-color: #FFB6B2; color: black;',
                #         2: 'background-color: #F0867D; color: black;',
                #         3: 'background-color: #EC5147; color: black;'
                #     }
                #     return [colors.get(row['공격 위험도'], '')] * len(row)

                # styler = styler.applymap(apply_style)

                # # 표 생성
                # st.table(styler)
                                # styler=last.style.format()
                # st.write(styler.to_html(), unsafe_allow_html=True)
                #last_no_index = last.reset_index(drop=True)
                #st.table(last_no_index)

                #st.table(last_without_index)\
                #def apply_style(row):
                        # "매우 위험한 단계입니다.\n 자동으로 로그인 차단을 실행합니다.": 'background-color: #EC5147;',
                        # "주의 단계입니다.\n 자동으로 일부 기능 차단을 실행합니다.": 'background-color: #F0867D;',
                        # "경계 단계입니다.\n 지속적인 경계가 필요합니다.": 'background-color: #FFB6B2;',
                        # "정상입니다." : 'background-color: #FFDBD9;',
                # colors = {
                #         '0': 'background-color: #FFDBD9;',
                #         '1': 'background-color: #FFB6B2;',
                #         '2': 'background-color: #F0867D;',
                #         '3': 'background-color: #EC5147;'
                #     }
                # #return [color_mapping.get(row, '') for row in test]
                #     #return [background_color_mapping.get(row['memo'], '') for row in test]
                
                # styler=last.style
                # styler = styler.apply(lambda row: [colors.get(row['공격 위험도'], '')]*len(row), axis=1)
                # #styler=styler.set_index(['공격 위험도','사용자 ID','memo'])
                # # 표 생성
                # st.table(styler)
                # styler2=last.style
                # styler2.set_properties(**{'color': 'black'})

                # # 표 생성
                # st.table(styler2)

                # styler_combined = styler.use(styler2)

                # # 표 생성
                # st.table(styler_combined)
                # styled_data = data3.style.set_table_styles(styles).apply(apply_style, axis=1)
                # styled_data.index.name = '사용자 ID'
                # styled_data = styled_data.set_table_attributes('border="1" class="dataframe"')
                # return styled_data
                #st.table(appy_style(data3, test, fig))
                    
                    #return ['text-align: center; color: black;' if col in ['공격 위험도', 'memo'] else background_color_mapping.get(row['memo'], '') for col in row.index]
                    
                #  for i, row in data.iterrows():
                #         styled_data.at[i, 'memo'] = background_color_mapping.get(row['memo'], '')
            
                #     styled_data = styled_data.style.applymap(lambda x: 'text-align: center; color: black' if x.name in ['공격 위험도', 'memo'] else '', subset=['공격 위험도', 'memo'])
        
                #     styled_data.set_properties(**{'border-color': 'black', 'text-align': 'center'})

                # styled_ldaa = last.style.apply(apply_style, axis=1)

                # styled_data.set_properties(**{'border-color': 'black',  'text-align': 'center'})
    
                #styled_last.set_table_styles([{'selector': 'th', 'props': [('color', 'black')]}])
                
                    # st.table(styled_data)
                    # st.markdown("<style>table td {text-align: center; color: black;}</style>")
            st.write("")        
            st.write("공격 위험도는 다음 요소에 따라 산정됩니다")
            st.write("")
            st.write("업무시간 외 로그인 여부, 소스코드 첨부 여부, DB 접근 빈도, 권한 상승 시도 여부 +a")
     
                # styled_last.set_properties(**{'border-color': 'black', 'text-align': 'center'})
                # st.table(styled_last)
                # st.markdown("<style>table td {text-align: center;}</style>", unsafe_allow_html=True)
                #styled_last = last.style.apply(apply_style, axis=1)
                #styled_last.set_properties(**{'border-color': 'black', 'text-align':'center'})
                ##styled_last.set_table_styles([{'selector': 'th', 'props': [('color', 'black')]}])
                #st.table(styled_last)
                #st.markdown("<style>table td {text-align: center;}</style>", unsafe_allow_html=True)
                #st.write(styled_last)
                #st.write("공격 위험도는 다음 요소에 따라 산정됩니다")
                #st.write("")
                #st.write("업무시간 외 로그인 여부, 소스코드 첨부 여부, DB 접근 빈도, 외부주소로 이메일 전송 수, 권한 상승 시도 여부 등")

              
                # 두 개의 컬럼 생성
        else:
            pass
    else:
        pass

    # HTML 코드를 생성하여 표시
   
   
    


# 메인 함수 호출
main()