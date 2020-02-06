from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


# Create your tests here.
def create_question(question_text, days):
    """
    Создаёт вопрос с переданным 'question_text' и датой публикации, которую передают в 'days' рассчитывая от текущего
    времени (отрицательное значение для вопросов, которые публиковались в прошлом, положительное для вопросов, которые
    еще будут опубликованы.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionResultsViewTests(TestCase):
    def test_future_question(self):
        """
        results view вопроса с датой будущей публикации вернет 404.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('mysite:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        results view вопроса с датой публикации в прошлом отображает результаты вопроса.
        """
        past_question = create_question(question_text='Past question.', days=-5)
        url = reverse('mysite:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        detail view вопроса с датой будущей публикации вернет 404.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('mysite:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        detail view вопроса с датой публикации в прошлом отображает текст вопроса.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('mysite:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Если вопрсов не существует, то показывает соответствующее сообщение.
        """
        response = self.client.get(reverse('mysite:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Доступных вопросов нет.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Вопросы с pub_date в прошлом отображаются на главной странице.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('mysite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Вопросы с pub_date в будущем не отображаются на главной странице.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('mysite:index'))
        self.assertContains(response, "Доступных вопросов нет.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Если существуют прошлые вопросы и будущие, только прошлые вопросы отображаются.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('mysite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        Главная страница с вопросами может отображать несколько вопросов.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('mysite:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращает False для вопросов, у которых pub_date в будущем времени.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возращает False для вопросов, у которых pub_date старше, чем 1 день.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возращает True для вопросов, у которых pub_date в течение последнего дня.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)
