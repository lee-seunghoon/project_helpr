import paho.mqtt.client as mqtt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import numpy as np
import re
from konlpy.tag import Okt, Mecab
from gtts import gTTS

LED = 21


class Led_Mqtt():
    def __init__(self,state,led_out,led_on,pwm):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("13.209.193.138", 1883, 60)

        client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        print("connect.." + str(rc))
        if rc == 0:
            client.subscribe("stt/test")
        else:
            print("connect fail..")

    def on_message(self, client, userdata, msg):
        self.myval = msg.payload.decode("euc-kr")
        msg = self.myval

        DATA_PATH = './data_in/Total_chat_data.csv'
        df = pd.read_csv(DATA_PATH, encoding='utf-8')

        q_prepro = df['question'].map(self.text_preprocessing)
        a_prepro = df['answer'].map(self.text_preprocessing)
        new_df = pd.concat([q_prepro, a_prepro], axis=1)

        new_df['question'] = new_df['question'].map(self.tokenize)

        result, sel_q, cosine = self.predict(msg, new_df, df)

        print(msg, '/', sel_q, '/', cosine, '/', result)

        tts = gTTS(text=result, lang='ko')
        tts.save('test.wav')

        # pub = mqtt.Client('python_pub')
        # pub.connect("13.209.193.138", 1883, 60)
        # pub.publish('stt/answer', result)

    def text_preprocessing(self, text):
        sentence = text.split(' ')
        total_sentence = []
        for word in sentence:
            prepro_word = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z]', '', word)
            total_sentence.append(prepro_word)
        result = ''.join(total_sentence)
        return result

    def tokenize(self, text):
        okt = Okt()
        mecab = Mecab('C:\mecab\mecab-ko-dic')
        tokens = mecab.pos(text)
        total_words = []
        for word, tag in tokens:
            if tag not in ['JKS', 'EC', 'JKB', 'JX', 'EP', 'NNB', 'VCP', 'ETM']:
                total_words.append(word)
        result = ' '.join(total_words)
        return result

    def cos_answer(self, new_q, new_df, df):
        tfidf = TfidfVectorizer()
        new_q = pd.Series(new_q)
        all_q = new_df.question.append(new_q)
        tfidf_matrix = tfidf.fit_transform(all_q)
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        questions = cosine_sim[-1][:-1]
        if 1. in questions:
            indices = np.where(questions == 1.)
            indices = indices[0].tolist()
            q_idx = np.random.choice(indices, 1)
            return df.question[q_idx[0]], df.answer[q_idx[0]], questions[q_idx[0]]
        elif max(questions) < 0.45:
            return None, '아직 정확하게 답변하기 어려워요', max(questions)
        else:
            q_idx = questions.argsort()[-1]
            return df.question[q_idx], df.answer[q_idx], questions[q_idx]

    def predict(self, question, new_df, df):
        real_question = []
        real_answer = []
        sel_q = []
        cos = []

        new_q = self.text_preprocessing(question)
        new_q = self.tokenize(new_q)

        selected_question, selected_answer, cosin = self.cos_answer(new_q, new_df, df)

        real_question.append(question)
        real_answer.append(selected_answer)
        sel_q.append(selected_question)
        cos.append(cosin)

        result = pd.DataFrame({
            'question': real_question,
            'selected_question': sel_q,
            'cosine_similarity': cos,
            'answer': real_answer
        })

        return real_answer[0], sel_q[0], cos[0]


if __name__ == "__main__":
    try:
        mymqtt = Led_Mqtt(0,None,None,None)

    except KeyboardInterrupt:
        print("종료")
        # GPIO.cleanup()

