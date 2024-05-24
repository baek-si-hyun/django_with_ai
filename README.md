<br>
<br>
<br>

![logo-lettering](https://github.com/DianaKang0123/selleaf/assets/156397873/b5f4c8cd-6d88-4965-9336-ad89f151ba52)
<br>
<br>
<br>

# 머신러닝 웹 적용 프로젝트

<br>
<br>
<br>

![image-6](https://github.com/baek-si-hyun/selleaf-server/assets/107901109/b2d7bb2c-4d6b-45bf-8f84-79c22a49c199)

<br>

## 나이브 베이즈 텍스트 분류를 통한 비속어 감지 시스템

### **0️⃣ 목차**

1. 개요
2. 데이터 수집
3. 데이터 전처리
4. 댓글 입력시 욕설 분석
5. 문제 댓글 신고 시 실시간 학습
6. 욕설 분석 알고리즘 흐름
7. 결과
8. 트러블 슈팅
9. 느낀점

<br>

---

<br>

### **1️⃣ 개요**

<br>

#### 셀리프는 커뮤니티 서비스를 제공합니다. 
자유롭게 게시글을 올릴수 있고 해당 게시물에 댓글을 작성할 수 있습니다.

> **나이브 베이즈 텍스트 분류를 통한 비속어 감지 시스템**은 일반 게시물의 댓글에 적용되며, **일반 게시글 댓글 작성** 단계에서 유저가 작성하는 댓글의 내용을 단어로 분할하여 벡터화 시키고 백터화된 데이터를 나이브 베이즈 분류기에 입력하여 비속어 여부를 예측합니다. 예측 결과에 따라 댓글에 비속어를 포함하고 있는지 판단합니다.

<br>

---

<br>

### **2️⃣ 데이터 수집**

<br>

#### 데이터를 수집하는 과정은 다음과 같습니다.

1. 크롤링을 통한 댓글 데이터 수집

- 크롤링을 통하여 댓글을 수집하고 비속어가 포함된 댓글과 포함되지 않은 댓글의 비중을 맞춰주기 위해 전체 댓글 데이터의 45%를 임의로 욕설을 추가합니다.

    <details>
    <summary>크롤링 로직</summary>

  ```
  if __name__ == '__main__':
      warnings.filterwarnings('ignore')

      if os.path.exists('comments.csv'):
          existing_df = pd.read_csv('comments.csv', encoding='utf-8-sig', index_col=0)
          comment_final = existing_df['Comment'].tolist()
      else:
          existing_df = pd.DataFrame()
          comment_final = []

      driver = webdriver.Chrome()
      driver.get("https://www.youtube.com/watch?v=t7w3k3pjZY4")
      driver.implicitly_wait(3)

      time.sleep(1.5)

      driver.execute_script("window.scrollTo(0, 800)")
      time.sleep(3)

      last_height = driver.execute_script("return document.documentElement.scrollHeight")

      while True:
          driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
          time.sleep(2)

          new_height = driver.execute_script("return document.documentElement.scrollHeight")
          if new_height == last_height:
              break
          last_height = new_height

      time.sleep(1.5)

      html = driver.page_source
      soup = BeautifulSoup(html, 'html.parser')

      comment_list = soup.select("span.yt-core-attributed-string")

      for i in range(len(comment_list)):
          temp_comment = comment_list[i].text.replace('"', '')
          temp_comment = temp_comment.replace('\n', ' ')
          temp_comment = temp_comment.strip()
          comment_final.append(temp_comment)
      new_df = pd.DataFrame({'Comment': comment_final})

      combined_df = pd.concat([existing_df, new_df]).drop_duplicates().reset_index(drop=True)

      combined_df.to_csv('qweqwe.csv', index=True, encoding='utf-8-sig')

      driver.quit()
  ```

    </details>
    <br>
    <details>
    <summary>임의로 욕설을 추가하는 코드</summary>

  ```
  profanity_list = ['욕설 리스트']

  def add_random_profanity(comment):
      new_comment = ''
      for word in comment.split():
          new_comment += word + ' '
          if random.random() < 0.4:
              profanity = random.choice(profanity_list)
              if random.random() < 0.5:
                  new_comment += profanity + ' '
              else:
                  new_comment += profanity
      return new_comment.strip()

  co_df = pd.read_csv('comments.csv')

  co_df['Comment'] = co_df['Comment'].apply(add_random_profanity)
  ```

    </details>
    <br>
    <details>
    <summary>추가한 욕설이 있으면 Target 칼럼에 1 없으면 0 값 넣어주기</summary>

  ```
  profanity_list = ['욕설 리스트']

  profanity_list = [word.replace(' ', '') for word in profanity_list]

  co_df['Profanity'] = co_df['Comment'].apply(lambda x: 1 if any(word in x for word in profanity_list) else 0)
  ```

    </details>

  <br>

2. 데이터세트를 통한 수집

- 직접 댓글 데이터 세트를 수집
- 데이터 세트 깃허브 주소: https://github.com/2runo/Curse-detection-data
- 댓글 내용과 타겟이 `|`로 구분되어 있는 데이터 세트로 read_csv 시 `sep='|'`을 사용
  <details>
    <summary>Click to see full code</summary>

        import pandas as pd

        reply_df = pd.read_csv('./datasets/dataset.txt', sep='|')
        reply_df

  </details>

  <br>

3. 두 데이터 세트 합치기

- 수집한 두 데이터 세트를 합치고 결과를 csv파일로 내보냅니다.

    <details>
    <summary>두 데이터 세트를 합치는 코드</summary>

  ```
      df_combined = pd.concat([co_df, bw_df], ignore_index=True)
  ```

    </details>
    <br>
    <details>
    <summary>결과를 CSV 파일로 내보내는 코드</summary>

  ```
      df_combined.to_csv('merge_comments_data.csv', index=False, encoding='utf-8-sig')
  ```

    </details>

  <br>

---

<br>

### **3️⃣ 데이터 전처리**

<br>

#### 데이터 전처리 과정은 다음과 같습니다.

1.  단어별로 분할하여 학습하는 나이브 베이즈 분류기의 특성을 고려해 모델의 성능을 향상 시키기 위해서는 불용어를 제거하였습니다. 또한 한글, 영어에 대한 비속어를 예측하는 모델을 만들기 위해 한글, 영어, 숫자를 제외한 특수문자, 이모티콘, 타 언어를 제거하였습니다.
    <details>
    <summary>한글, 영어, 숫자를 제외한 문자들을 제거하는 코드</summary>

    ```
        korean_stopwords = set([
            '이', '그', '저', '것', '들', '의', '를', '은', '는', '에', '와', '과', '도', '으로', '까지', '부터', '다시', '번', '만', '할', '한다', '그리고'
        ])

        # 데이터 전처리 함수 정의
        def preprocess_text(text):
            # 특수 문자 제거
            text = re.sub(r'[^가-힣a-zA-Z0-9\s-]', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            # 형태소 분석
            words = text.split()
            # 불용어 제거
            text = ' '.join([word for word in words if word not in korean_stopwords])
            return text

        # 데이터 전처리 적용
        reply_df['Comment'] = reply_df['Comment'].apply(preprocess_text)
        reply_df['Comment'].replace('', pd.NA, inplace=True)
        reply_df.dropna(subset=['Comment'], inplace=True)

    ```

    </details>
    <br>

2.  중복과 null인 값을 확인하고 제거하였습니다.
    <details>
    <summary>중복과 null값 존재 확인 및 제거하는 코드</summary>

    ```
    print(reply_df.duplicated().sum())
    reply_df.drop_duplicates(inplace=True)

    display(reply_df[reply_df['Comment'].isna()])
    reply_df = reply_df.dropna(subset=['Comment'])
    ```

    </details>

    <br>

3.  Target 데이터의 비중을 맞췄습니다.
    <details>
    <summary>Target 비중을 확인하고 언더 샘플링하는 코드</summary>

        ```
            print(reply_df.Target.value_counts())

            profanity = reply_df[reply_df['Target'] == 1].sample(8151, random_state=124)
            normal = reply_df[reply_df['Target'] == 0]
            reply_df = pd.concat([profanity, normal]).reset_index(drop=True)
        ```

    </details>
    <br>

    <br>

---

<br>

### **4️⃣ 댓글 입력시 욕설 분석**

#### 댓글 입력시 욕설 분석 알고리즘은 다음과 같습니다.

1. 화면에서 입력된 댓글을 post-module.js의 write 함수에서 fatch 를 통해 post 방식으로 전달
   <details>
   <summary>write 함수 코드</summary>

   ```
       const write = async (reply) => {
           const response = await fetch("/post/replies/write/", {
               method: "POST",
               headers: {
                   'Content-Type': 'application/json;charset=utf-8',
                   'X-CSRFToken': csrf_token
               },
               body: JSON.stringify(reply)
           });
           return response.json()
       }
   ```

   </details>

<br>

2. view 에서 사전 훈련된 모델로 비속어 검사
   <details>
   <summary>전달 받은 댓글 내용 비속어 검사 코드</summary>

   ```
       class PostReplyWriteApi(APIView):
           @transaction.atomic
           def post(self, request):
               data = request.data
               post = Post.objects.filter(id=data['post_id']).values('member_id')

               new_sentence = [data['reply_content']]

               prediction = profanityDetectionPredict(new_sentence)
   ```

   </details>
   <br> 
   <details>
   <summary>모듈화된 비속어 검사 코드</summary>

   ```
       model_path = os.path.join(Path(__file__).resolve()\
           .parent, '../../ai/ai/commentai.pkl')
   ```


        def profanityDetectionPredict(new_sentence):
            loaded_model = joblib.load(model_path)

            prediction = loaded_model.predict(new_sentence)
            return prediction
    ```

    </details>

<br>

3. 비속어가 포함되어 있을 않을 경우(prediction[0]가 0일 경우) 해당 게시물에 댓글이 추가되는 코드
   <details>
   <summary>비속어가 포함되지 않았을 경우 코드</summary>

   ```
       message = 'fails'
           if prediction[0] == 0:
               message = 'ok'

               data = {
                   'post_reply_content': new_sentence[0],
                   'post_id': data['post_id'],
                   'member_id': request.session.get('member')['id']
               }

               PostReply.objects.create(**data)
   ```

   </details>

<br>

4. 비속어가 포함되어 있을 경우 해당 댓글로 모델의 추가학습을 진행하고 훈련 전용 테이블에 추가하는 코드
   <details>
   <summary>비속어가 포함되어있을 경우 추가학습 시키는 코드</summary>

   ```
           else:
               data = {
                   'comment': new_sentence[0],
                   'target': 1,
               }

               profanityDetectionModel(new_sentence)

               AiPostReply.objects.create(**data)

           return Response(message)
   ```

   </details>
   <br>    
   <details>
   <summary>모듈화된 추가학습 시키는 코드</summary>

   ```
       model_path = os.path.join(Path(__file__).resolve()\
           .parent, '../../ai/ai/commentai.pkl')

       def profanityDetectionModel(new_sentence):
           loaded_model = joblib.load(model_path)
           transformed_X_train = loaded_model.named_steps['count_vectorizer']\
               .transform(new_sentence)
           loaded_model.named_steps['multinomial_NB']\
               .partial_fit(transformed_X_train, [1])
           joblib.dump(loaded_model, model_path)
   ```

   </details>

<br>

---

<br>

### **5️⃣ 문제 댓글 신고 시 실시간 학습**

#### 댓글 신고시 욕설 처리 알고리즘은 다음과 같습니다.

1. 신고된 댓글을 처리하는 view에서 신고받은 댓글을 일반 게시물 댓글 신고 테이블에 추가
   <details>
   <summary>일반 게시물 댓글 신고 테이블에 추가 코드</summary>

   ```
       class PostReplyReportView(View):
           def post(self, request):
               data = request.POST
               member = request.session.get('member')['id']
               member_id = member.get('id')
               post_id = request.GET['id']
               reply_id = data['reply-report-reply-id']

               datas = {
                   'member_id': member_id,
                   'post_reply_id': reply_id,
                   'report_content': data['reply-report-content']
               }

               PostReplyReport.object.create(**datas)

               return redirect(f'/post/detail/?id={post_id}')
   ```

   </details>

<br>

2. 관리자 페이지에서 신고된 댓글을 확인하고 신고당한 댓글을 삭제 처리하는 view에서 삭제하기전 해당 욕설 댓글로 모델을 추가학습을 진행, 일반 댓글 테이블에서 삭제하고 모델 훈련 테이블에 추가
   <details>
   <summary>삭제하기전 해당 욕설 댓글로 모델을 추가학습을 진행하는 코드</summary>

   ```
       def delete(self, request, report_ids):
           report_ids = report_ids.split(',')

           for report_id in report_ids:
               if report_id != '':
                   post_report_reply = PostReplyReport.object.filter(id=report_id)\
                       .values().first()
                   report_reply_id = post_report_reply.get('post_reply_id')
                   post_reply = PostReply.objects.filter(id=report_reply_id)\
                       .values().first()

                   new_sentence = [post_reply['post_reply_content']]
                   profanityDetectionModel(new_sentence)

   ```

   </details>
   <br> 
   <details>
   <summary>일반 댓글 테이블에서 삭제하고 모델 훈련 테이블에 추가하는 코드</summary>

   ```
                   data = {
                       'comment': new_sentence[0],
                       'target': 1,
                   }
                   AiPostReply.objects.create(**data)

                   PostReplyReport.object.get(id=report_id).delete()
                   PostReply.objects.get(id=report_reply_id).delete()
   ```

   </details>

<br>

---

<br>

### **6️⃣ 욕설 분석 알고리즘 흐름**

<br>

#### 욕설 분석 알고리즘의 흐름은 다음과 같습니다.

1. 화면에서 비속어가 포함되어 있는 댓글 입력

   > ![image](https://github.com/baek-si-hyun/selleaf-server/assets/107901109/e971451c-f718-4bcf-9b16-86e6b6713036)

2) 입력 클릭시 post-module.js이 write를 통하여 해당 정보 post 방식으로 view에 전달
3) view에서 사전학습된 모델을 통해 비속어 포함 유무를 검사하고 결과를 return (비속어가 포함된 경우 추가학습후 return)
4) return된 값을 post-module에서 write함수의 fetch를 통해 response로 return
5) return으로 전달받은 response 데이터를 활용하여 '비속어가 포함되었습니다' 문구 화면에 출력

   > ![image-3](https://github.com/baek-si-hyun/selleaf-server/assets/107901109/24face29-414c-4474-bd27-db0fbbffaac3)

6. 비속어가 포함하여 댓글을 작성할 수 없으므로 사용자는 정상적인 댓글을 입력하게 됨
7. 비속어를 사전학습 모델이 감지하지 못할 경우 신고 기능을 통해 관리자에게 비속어 댓글이 있음을 알림

   > ![image-3](https://github.com/baek-si-hyun/selleaf-server/assets/107901109/7314b731-49b4-480c-8b46-75560aaaaedb)

8. 관리자가 해당 신고를 확인하고 비속어 댓글을 삭제시 추가학습 진행후 삭제처리 (모델 훈련 테이블에는 추가)

   > ![image-3](https://github.com/baek-si-hyun/selleaf-server/assets/107901109/74dd3564-d68b-42ff-90cd-d2595dd3f2df)

9. 감지하지 못한 비속어를 학습함으로 모델의 비속어 감지 능력 향상

---

<br>

### **7️⃣ 결과**

<br>

> #### 🚩 비속어 댓글
>
> <img src="https://github.com/baek-si-hyun/selleaf-server/assets/107901109/24face29-414c-4474-bd27-db0fbbffaac3" width="600px">

> #### 🚩 비속어 댓글 신고
>
> <img src="https://github.com/baek-si-hyun/selleaf-server/assets/107901109/7314b731-49b4-480c-8b46-75560aaaaedb" width="300px">

> <img src="https://github.com/baek-si-hyun/selleaf-server/assets/107901109/06149d04-cc85-4d48-8a88-06881b3f0b63" width="300px">
> <img src="https://github.com/baek-si-hyun/selleaf-server/assets/107901109/74dd3564-d68b-42ff-90cd-d2595dd3f2df" width="500px">
> <img src="https://github.com/baek-si-hyun/selleaf-server/assets/107901109/d98c7474-1837-418a-af16-d2814ab48d18" width="500px">

---

<br>

### **8️⃣ 트러블 슈팅**

<br>
<br>

#### 1. 사전 훈련 모델이 입력 받은 단어와 상관없이 모두 비속어라고 예측

❗ 문제

- 사전 학습 모델을 적용하여 비속어 댓글 직접 입력해 테스트하는 과정에서 사전 학습 모델이 입력 받은 단어와 상관없이 모두 비속어가 포함 되어있다고 예측하는 문제 발생
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/8d9d0f88-77bf-4779-80d5-af1bb1a0e82e" width="500px">
  >
  > <small>1은 비속어가 포함 되어 있다는 것을 의미한다.</small>
  >
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/2677ef68-50e5-4f16-9b7b-35ac3c015a0f" width="100px">

<br>

❓ 원인

- <code>.fit</code> 전체 데이터를 한번에 학습 시키는 메서드이다. <code>.fit</code>메서드를 사용해 사전 훈련을 진행한 상태이다.
- 화면에서 전달받은 문장을 추가학습 시켜야 하는데 <code>.fit</code>이라는 동일한 메서드를 사용하여 기존 사전 훈련을 받은 모델에 추가학습이 아닌 덮어쓰기가 진행되었다.
- 이로 인해 데이터가 하나인 훈련모델이 되어 위와같은 문제가 발생 되었다.

![p_fit](https://github.com/baek-si-hyun/django_with_ai/assets/107901109/58f89411-f224-4e58-b817-24a0ba66a5de)

- 화면에서 전달 받은 문장 하나로 이미 훈련된 모델에 전체 데이터 학습을 진행 시켰다.
- 기존에 사전 훈련받은 모델의 데이터는 다 사라지고 전달 받은 문장 데이터 하나로 훈련된 모델이 되었다.

<br>

✔ 해결

- 전체 데이터를 학습 시키는 <code>.fit</code>메서드를 사용하지 않고 기존에 훈련되어 있는 모델에 추가로 학습을 진행시키는 <code>.partial_fit</code>메서드를 사용하여 해결하였다.
  >
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/3e125e8c-f834-49d4-96d1-bba752a4640e" width="500px">
  > <br><br>
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/8d9d0f88-77bf-4779-80d5-af1bb1a0e82e" width="500px">
  > 
  > <small>0은 비속어가 포함 되어있지 않다는 것을 의미한다.</small>
  >
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/710c12e2-2bda-418f-9cfa-aafd2f2ce09c" width="100px">

<br>
<br>

### 2. 너무 낮은 정확도로 인한 비속어 예측 무의미

❗ 문제

- 사전 훈련 모델의 평가 지표가 정확도, 정밀도 재현율, f1 score 모두 0.60 ~ 0.63 으로 낮은 수치를 보여주었다.
- 불용어('의', '를', '은', '는', '에', 등) 의미를 전달하지 않는 용어들을 전처리 과정에서 제거 하였는데도 수치에 변화가 없었다.

<br>

❓ 원인

- 타 팀들의 댓글 비속어 감지 시스템 담당자들과 소통한 결과 데이터 세트 수가 5000개로 모델이 학습하기에는 적다고 판단했다.

<br>

✔ 해결

- 서로의 데이터 세트를 통합하고 추가로 데이터를 수집해 10000개가 넘는 데이터 세트를 제작하였다.
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/77af3f38-231d-445d-a22e-e503c7f134c9" width="500px" >

<br>

- 한국어, 영어, 숫자를 제외한 문자들은 빈문자열로 대체를 하는 전처리 과정을 추가하였다.
  >
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/413f2b08-454e-464c-9b57-8856657ceef7" width="500px" >

<br>

- 데이터의 수를 늘리고, 전처리 과정을 통해 목표 수치였던 0.7을 넘기며 문제를 해결하였다.
  > <img src="https://github.com/baek-si-hyun/django_with_ai/assets/107901109/af3e1ac9-8dbf-411e-9250-adc160c6abd3" width="700px" >

<br>

### **9️⃣ 느낀점**

- 직접 수집한 데이터였기에 노이즈가 많았고 이는 훈련 모델에 부정적인 영향을 끼쳐 평가지표의 수치를 높이는데 어려움이 있었습니다. 다른 댓글 시스템 담당자와 협업하며 최적의 모델을 만들기 위해 다양한 전처리와 모델 튜닝을 경험하며 
잘 정제된 데이터의 중요성을 느꼈고 또한 전처리 과정에서의 세심한 접근이 얼마나 중요한지 깨닫게 되었습니다.

- 인공지능을 직업 상용화해보면서 인공지능의 이점들을 몸으로 느낄 수 있었습니다. 제가 맡은 댓글 관리는 전부 사람이 직접 한다면 많은 인력과 비용이 낭비되는 파트입니다. 하지만 AI가 대부분 이를 대신하게 되면서 기업 입장에서 왜 AI를 도입하려는지 몸으로 느낄 수 있었고, 신고 기능을 통해 모델에 추가 학습을 진행하면 할수록 더욱 정교해지는 인공지능을 보며, AI의 학습 능력과 적응력이 얼마나 뛰어난지 깨닫게 되었습니다.