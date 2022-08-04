from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import Restarted, EventType, UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import random
class GetRandomName():
    def __init__(self):
        self.name_recom = ""
        numberlist = random.sample(range(0, len(NAME) - 1), 5)
        for i in numberlist:
            self.name_recom += NAME[i]


class ActionGreeting(Action):
    def name(self) -> Text:
        return "action_greeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:


        dispatcher.utter_message( response="utter_greet_2")

        dispatcher.utter_message(response="utter_greet_3")

        greet_4 = "^_^ Here are some fictitious name options for you. " \
                  "you can type the name that you want to use: \n"

        dispatcher.utter_message(text= greet_4 + GetRandomName().name_recom)
        return []


class ValidateProfileForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_make_profile_form"
    def validate_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        user_name = next(tracker.get_latest_entity_values("name"), None)
        print(user_name)
        if user_name not in NAME_LIST:
            msg = "Sorry🤗, This name is not in our database. Please select the name in the list: \n"
            dispatcher.utter_message(text=msg + GetRandomName().name_recom)
            return {"name": None}
        dispatcher.utter_message(response="utter_set_name", name=user_name)
        return {"name": user_name}
    def validate_gender(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        user_gender = next(tracker.get_latest_entity_values("gender"), None)
        print(user_gender)
        GENDER = ["female", "male"]
        if user_gender not in GENDER:
            msg = "Sorry🤗, Please type female or male as your fictitious gender"
            dispatcher.utter_message(text=msg)
            return {"gender": None}
        dispatcher.utter_message(response="utter_set_gender", gender=user_gender)
        return {"gender": user_gender}

    def validate_age(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        user_age = next(tracker.get_latest_entity_values("age"), None)
        print(user_age)
        if int(user_age) > 100:
            msg = "Sorry🤗, Please type right age"
            dispatcher.utter_message(text=msg)
            return {"age": None}
        if int(user_age) < 18:
            msg = "Sorry🤗, Please type age over 18"
            dispatcher.utter_message(text=msg)
            return {"age": None}
        dispatcher.utter_message(response="utter_set_age", age=user_age)
        return {"age": user_age}

    def validate_condition(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        user_condition = next(tracker.get_latest_entity_values("condition"), None)

        if user_condition not in CONDIT:
            msg = "Sorry🤗, Please choose the condition in the list"
            dispatcher.utter_message(text=msg)
            return {"condition": None}
        dispatcher.utter_message(response="utter_set_condition", condition=user_condition)
        return {"condition": user_condition}


class ActionSetProfile(Action):
    def name(self) -> Text:
        return "action_set_profile"
    def __init__(self):
        self.button = []
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        user_name = tracker.get_slot('name')
        user_gender = tracker.get_slot('gender')
        user_age = tracker.get_slot('age')
        user_condition = tracker.get_slot('condition')

        dispatcher.utter_message(
            response="utter_set_profile",
            name=user_name,
            gender=user_gender,
            age=user_age,
            condition=user_condition )
        self.button = RecommendQuery(user_condition,user_gender,user_age).get_redcommend()

        message = "Here are some recommended questions for you:"
        if len(self.button) < 1:
            msg = "You can ask me questions about:" \
                  "**Covid Test**, **Covid Symptoms**, **Covid Treatment**, " \
                  "**Covid Self-isolation**, **Covid Risk**,**Covid Vaccine**, **Other**."
            dispatcher.utter_message(text=msg,buttons= self.button)
        elif len(self.button) == 1:
            dispatcher.utter_message(text=message, buttons=self.button[0])
        else:
            dispatcher.utter_message(text=message, buttons=self.button[0]+self.button[1])
            # dispatcher.utter_message(buttons=self.button[1])

        return []
class RecommendQuery():
    def __init__(self,condition,gender,age):
        self.button = []
        self.condition = condition
        self.gender = gender
        self.age = int(age)
    def get_redcommend(self):
        if self.condition:
            if self.condition == "cancer":
                self.button.append(CANCER_BUTTON)
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
            if self.condition == "diabetes":
                self.button.append(DIABETES_BUTTON)
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
            if self.condition == "kidney disease":
                self.button.append(KIDNEY_BUTTON)
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
            if self.condition == "immunodeficiency":
                self.button.append(IMMU_BUTTON)
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
            if self.condition == "lung disease":
                self.button.append(LUNG_BUTTON)
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
            if self.condition == "none":
                if 55 > self.age > 25 and self.gender == "female":
                    self.button.append(PREG_BUTTON)
                if self.age > 55:
                    self.button.append(OLD_BUTTON)
        return self.button

class ActionDefaultAskAffirmation(Action):
    def name(self):
        return "action_default_ask_affirmation"
    def __init__(self) -> None:
        self.intent_mappings = INTENT
    async def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
            ) -> Dict[Text, Any]:
        # select the top three intents from the tracker
        # ignore the first one -- nlu fallback  == tracker.latest_message["intent_ranking"][1:4]
        predicted_intents = tracker.latest_message["intent_ranking"][1:2]
        predict = []

        if predicted_intents[0]["confidence"] > 0.1:
            if len(predicted_intents[0]["name"]) > 10 \
                    and predicted_intents[0]["name"] != "ask_covid_question_type"\
                    and predicted_intents[0]["name"] != "out_of_scope"\
                    and predicted_intents[0]["name"] != "bot_challenge":
                predict.append(predicted_intents[0])

        if len(predict) > 0:
            # print(predict)
            # A prompt asking the user to selectan option
            message = "I'm not sure I've understood you correctly 🤔 Do you mean..."
           # a mapping between intents and user friendly wordings
           # show the top three intents as buttons to the user
            buttons = [
                {
                    "title": self.intent_mappings[intent['name']],
                    "payload": "/{}".format(intent['name'])
                }
                for intent in predict
            ]
            # add a "none of these button", if the user doesn't
            # agree when any suggestion
            buttons.append({
                "title": "None of these",
                "payload": "/out_of_scope"
            })
            dispatcher.utter_message(text=message, buttons=buttons)
        else:
            dispatcher.utter_message(response="utter_default")
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:

        dispatcher.utter_message(response="utter_out_of_scope")

        return [UserUtteranceReverted()]


class ActionAskQuestionType(Action):
    def name(self) -> Text:
        return "action_covid_question_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        question_type = next(tracker.get_latest_entity_values("question_type"), None)

        if question_type not in QUESTION_TYPES:
            dispatcher.utter_message(text=f"Please check your spelling and try again !")
            return []
        else:
            msg = "Great! 🤗🤗 Here are some questions you might be interested in. You can also type in similar questions that you would like to know."

            if question_type == list(QUESTION_TYPES.values())[0]:
                dispatcher.utter_message(text=msg, buttons=TEST)
                return []

            if question_type == list(QUESTION_TYPES.values())[1]:
                dispatcher.utter_message(text=msg, buttons=SYMPTOM)
                return []

            if question_type == list(QUESTION_TYPES.values())[2]:
                dispatcher.utter_message(text=msg, buttons=TREATMENT)
                return []

            if question_type == list(QUESTION_TYPES.values())[3]:
                dispatcher.utter_message(text=msg, buttons=ISOLATION)
                return []

            if question_type == list(QUESTION_TYPES.values())[4]:
                dispatcher.utter_message(text=msg, buttons=RISK)
                return []

            if question_type == list(QUESTION_TYPES.values())[5]:
                dispatcher.utter_message(text=msg, buttons=VACCINE)
                return []

            if question_type == list(QUESTION_TYPES.values())[6]:
                dispatcher.utter_message(text=msg, buttons=OTHER)
                return []


class ActionCovidTestTypes(Action):
    def name(self) -> Text:
        return "action_covid_test_1"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You may want to know:"
        buttons_rs = [
            {
                "title": "What is the antigen test?",
                "payload": "/covid_test_2"
            },
            {
                "title": "What is PCR test?",
                "payload": "/covid_test_14"
            }
        ]
        dispatcher.utter_message(response="utter_covid_test_1", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


class ActionCovidTest14(Action):
    def name(self) -> Text:
        return "action_covid_test_2"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You may want to know:"
        buttons_rs = [
            {
                "title": "When can I do an antigen test?",
                "payload": "/covid_test_5"
            },
            {
                "title": "How to book an antigen test?",
                "payload": "/covid_test_6"
            }
        ]
        dispatcher.utter_message(response="utter_covid_test_2", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []

class ActionCovidTest5(Action):
    def name(self) -> Text:
        return "action_covid_test_5"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You may want to know:"
        buttons_rs = [
            {
                "title": "How to do an antigen test?",
                "payload": "/covid_test_4"
            },
            {
                "title": "How to book an antigen test?",
                "payload": "/covid_test_6"
            },
            {
                "title": "Do children need an antigen test?",
                "payload": "/covid_test_7"
            }
        ]
        dispatcher.utter_message(response="utter_covid_test_5", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


class ActionCovidSymptom1(Action):
    def name(self) -> Text:
        return "action_covid_symptom_1"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You can type in similar questions that you want to know 🤗.😋 You may want to know:."
        buttons_rs = [
            {
                "title": "What are the less common symptoms of covid?",
                "payload": "/covid_symptom_2"
            },
            {
                "title": "What are the serious symptoms of covid?",
                "payload": "/covid_symptom_3"
            },
            {
                "title": "Symptoms of dehydration?",
                "payload": "/covid_symptom_12"
            },
            {
                "title": "Symptoms for fatigue?",
                "payload": "/covid_symptom_19"
            }
        ]
        dispatcher.utter_message(response="utter_covid_symptom_1", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


class ActionCovidSymptom2(Action):
    def name(self) -> Text:
        return "action_covid_symptom_2"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You can type in similar questions that you want to know 🤗.😋 You may want to know:."
        buttons_rs = [
            {
                "title": "What should I do if I have covid symptoms?",
                "payload": "/covid_symptom_4"
            },
            {
                "title": "What should I do if my children have covid symptoms?",
                "payload": "/covid_symptom_5"
            },
            {
                "title": "What should I do if I have serious covid symptom?",
                "payload": "/covid_symptom_6"
            },
            {
                "title": "What should I do if I have a high fever from covid?",
                "payload": "/covid_symptom_7"
            }
        ]
        dispatcher.utter_message(response="utter_covid_symptom_2", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


class ActionCovidSymptom11(Action):
    def name(self) -> Text:
        return "action_covid_symptom_11"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You can type in similar questions that you want to know 🤗.😋 You may want to know:."
        buttons_rs = [
            {
                "title": "What should I do if I get dehydration from covid?",
                "payload": "/covid_symptom_10"
            },
            {
                "title": "What should I do if my children have covid symptoms?",
                "payload": "/covid_symptom_5"
            },
            {
                "title": "Lower the risk of dehydration?",
                "payload": "/covid_symptom_13"
            },
            {
                "title": "What should I do if I have a severe dehydration?",
                "payload": "/covid_symptom_14"
            }
        ]
        dispatcher.utter_message(response="utter_covid_symptom_11", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


class ActionOther1(Action):
    def name(self) -> Text:
        return "action_covid_other_1"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        msg = "You can type in similar questions that you want to know 🤗.😋 You may want to know:."
        buttons_rs = [
            {
                "title": "What kinds of test are available?",
                "payload": "/covid_test_1"
            },
            {
                "title": "What are the most common symptom of covid?",
                "payload": "/covid_symptom_1"
            },
            {
                "title": "The way to deal with covid at home?",
                "payload": "/covid_treatment_1"
            },
            {
                "title": "Why I need to do self-quarantine?",
                "payload": "/covid_isolation_1"
            },
            {
                "title": "Who are in the higher risk from covid-19?",
                "payload": "/covid_risk_1"
            },
            {
                "title": "What is COVID-19 vaccine?",
                "payload": "/covid_vaccine_1"
            }
        ]
        dispatcher.utter_message(response="utter_covid_other_1", buttons=buttons_rs)
        dispatcher.utter_message(text=msg, buttons=buttons_rs)

        return []


INTENT = {
    "greet":"Hi",
    "goodbye":"Bye",
    "affirm":"Yes",
    "deny":"No",
    "thanks":"Thanks",
    "out_of_scope":"I want a pizza",
    "bot_challenge":"Are you a bot",
    "ask_covid_question_type":"i want to know covid test",
    "covid_test_1":"What kinds of test are available?",
    "covid_test_2":"What is the antigen test?",
    "covid_test_3":"When can I do PCR test?",
    "covid_test_4":"How to do antigen test?",
    "covid_test_5":"When can I do an antigen test?",
    "covid_test_6":"How to book an antigen test?",
    "covid_test_7":"Do children need an antigen test?",
    "covid_test_8":"How to do an antigen test with children",
    "covid_test_9":"What should I do if my antigen test is positive",
    "covid_test_10":"What should I do if my antigen test is negative",
    "covid_test_11":"How to get a covid-19 recovery certificate",
    "covid_test_12":"What should I do if my PCR test is positive",
    "covid_test_13":"What should I do if my pcr test is invalid",
    "covid_test_14":"What is PCR test?",
    "covid_symptom_1":"What are the most common symptom of covid",
    "covid_symptom_2":"What is the less common symptoms of covid",
    "covid_symptom_3":"What is the serious symptoms of covid",
    "covid_symptom_4":"What should I do if I have covid symptoms",
    "covid_symptom_5":"What should I do if my children have covid symptoms",
    "covid_symptom_6":"What should I do if I have serious covid symptom",
    "covid_symptom_7":"What should I do if I have a high fever from covid",
    "covid_symptom_8":"More about high fever",
    "covid_symptom_9":"I want to learn more about children have a high fever",
    "covid_symptom_10":"What should I do if I get dehydration from covid",
    "covid_symptom_11":"More about dehydration",
    "covid_symptom_12":"Symptoms of dehydration",
    "covid_symptom_13":"Lower the risk of dehydration",
    "covid_symptom_14":"What should I do if I have a severe dehydration",
    "covid_symptom_15":"More about dehydration for children",
    "covid_symptom_16":"Children have a serious dehydration from covid",
    "covid_symptom_17":"The symptoms of dehydration in babies and children",
    "covid_symptom_18":"Lower the risk of dehydration for children",
    "covid_symptom_19":"Symptoms for fatigue",
    "covid_symptom_20":"Reduce tiredness and fatigue from covid",
    "covid_treatment_1":"The way to deal with covid at home ",
    "covid_treatment_2":"What can I take to treat my symptoms",
    "covid_treatment_3":"Does antibiotics work to covid symptoms",
    "covid_treatment_4":"Is ibuprofen good for covid symptoms",
    "covid_treatment_5":"How do I take care of my cough?",
    "covid_treatment_6":"What should I do if I have asthma health condition",
    "covid_treatment_7":"What should I do if I have shortness of breath",
    "covid_treatment_8":"What should I do if I lose my smell from covid",
    "covid_treatment_9":"More about Anti-inflammatory medicines",
    "covid_treatment_10":"More cough treatment for baby and children ",
    "covid_other_1":"What is COVID-19",
    "covid_other_2":"Who should get a COVID test",
    "covid_other_3":"what should I do if I start to feel unwell",
    "covid_isolation_1":"Why I need to do self-quarantine",
    "covid_isolation_2":"When I need to do self-quarantine",
    "covid_isolation_3":"What should I do for self-quarantine",
    "covid_isolation_4":"What I should not do in self-isolation",
    "covid_isolation_5":"How long do I need to do self-quarantine",
    "covid_isolation_6":"What should I do after 7 days of self-isolation",
    "covid_isolation_7":"When do my children need to quarantine",
    "covid_isolation_8":"How long does it take for children isolation",
    "covid_isolation_9":"How to deal with self-isolation",
    "covid_risk_1":"Who are in the higher risk from covid-19",
    "covid_risk_2":"Who are in the very high risk",
    "covid_risk_3":"More Information for high risk groups",
    "covid_risk_4":"More Information for very high risk groups",
    "covid_vaccine_1":"What is COVID-19 vaccine",
    "covid_vaccine_2":"Who need to get the covid vaccine",
    "covid_vaccine_3":"People who should not get Nuvaxovid vaccine",
    "covid_vaccine_4":"How many vaccine do I need for first round",
    "covid_vaccine_5":"Should I have an additional dose if I have a weak immune system",
    "covid_vaccine_6":"What do you think of getting a booster",
    "covid_vaccine_7":"Why is it important to get the covid vaccine?",
    "covid_vaccine_8":"Do I need to get the vaccine if I had covid",
    "covid_vaccine_9":"Can I get a vaccine if I have covid now",
    "covid_vaccine_10":"Can I get two vaccines at the same time",
    "covid_vaccine_11":"Who is my vaccinator",
    "covid_vaccine_12":"Does the vaccine give me covid",
    "covid_vaccine_13":"Can I get the vaccine if I have a high temperature",
    "covid_vaccine_14":"Can I get the covid vaccine if I am pregnant",
    "covid_vaccine_15":"Is the vaccine safe",
    "covid_vaccine_16":"How is the vaccine given",
    "covid_vaccine_17":"What are the side effects of the vaccine",
    "covid_vaccine_18":"What might happen in the few days if I get the vaccine",
    "covid_vaccine_19":"Why I get a fever after I take the vaccine",
    "covid_vaccine_20":"How long will the vaccine work",
    "covid_vaccine_21":"Does the vaccine work in everyone",
    "covid_vaccine_22":"Will I spread covid to others if I get the vaccine",
    "covid_vaccine_23":"How long does the Nuvaxovid vaccine last",
    "covid_vaccine_24":"Is the vaccine effective for children aged 5 to 11 years",
    "covid_vaccine_25":"Is the vaccine safe for children",
    "covid_vaccine_26":"How to get a covid vaccine",
    "covid_vaccine_27":"what is mRNA vaccine",
    "covid_vaccine_28":"more vaccine information for pregnant women",
    "covid_vaccine_29":"Recommended vaccines for pregnant women",
    "covid_vaccine_30":"More information for vaccine safety",
    "covid_vaccine_31":"Uncommon side effects of the vaccine",
    "covid_vaccine_32":"More information for vaccine side effects",
    "covid_diabetes_1":"Are people with diabetes more likely to get COVID-19?",
    "covid_diabetes_2":"Do people with diabetes have serious complications from COVID-19?",
    "covid_diabetes_3":"Do persons with type 1 and type 2 diabetes meet different risks?",
    "covid_diabetes_4":"Does COVID-19 cause diabetes?",
    "covid_diabetes_5":"What should diabetics do if they feel they are developing covid symptoms?",
    "covid_diabetes_6":"what should diabetics do if they have covid ?",
    "covid_diabetes_7":"What should diabetics do at home to avoid the spread of covid?",
    "covid_diabetes_8":"Can covid patients who are diabetic bring their own blood glucose monitors?",
    "covid_diabetes_9":"Should i stop taking certain blood pressure medication to lower my risk of covid?",
    "covid_diabetes_10":"How covid effect people with diabetes?",
    "covid_diabetes_11":"Advice for people with diabetes to protect themselves?",
    "covid_diabetes_12":"Is the risk of type 1 and type 2 diabetes the same?",
    "covid_kidney_1":"Is the COVID-19 vaccine safe for patients with kidney disease",
    "covid_kidney_2":"Are people with Chronic Kidney Disease at higher risk of complications?",
    "covid_kidney_3":"Should I continue my dialysis treatment and care team appointments?",
    "covid_kidney_4":"Does the COVID-19 vaccine affect the kidneys?",
    "covid_kidney_5":"Should rare kidney disease patients get the COVID-19 vaccine?",
    "covid_kidney_6":"will the covid vaccine effect kidney disease treatments and medications?",
    "covid_kidney_7":"Should family members of kidney and transplant patients wait to get vaccinated?",
    "covid_kidney_8":" Should people with End Stage Kidney Disease (ESKD) get the vaccine?",
    "covid_immunodeficiency_1":"Are COVID-19 vaccines safe for people with immunodeficiency?",
    "covid_immunodeficiency_2":"Do immunodeficiency treatments need to be stopped to have a COVID-19 vaccine?",
    "covid_immunodeficiency_3":"What precautions should people with immunodeficiencies take?",
    "covid_immunodeficiency_4":"Are people with immunodeficiency more likely to catch COVID-19?",
    "covid_immunodeficiency_5":"Would covid cause immunocompromised persons' immune systems to go into overdrive?",
    "covid_immunodeficiency_6":"Which of the COVID vaccines is best for people with primary and secondary immunodeficiency?",
    "covid_immunodeficiency_7":"Have any of the vaccine trials involved people with immunodeficiency?",
    "covid_immunodeficiency_8":"What are the benefits of getting a vaccine for people with immunodeficiency?",
    "covid_cancer_1":"Is it safe to get the COVID-19 vaccine while receiving cancer treatment?",
    "covid_cancer_2":"I have cancer, are there any risks associated with the COVID-19 vaccine?",
    "covid_cancer_3":"My cancer surgery is coming up soon. Should I take the COVID-19 vaccine?",
    "covid_cancer_4":"Will I need an additional dose of a COVID-19 vaccine, if i have a cancer?",
    "covid_cancer_5":"Is there a higher risk of side effects for people who are having chemotherapy or radiotherapy?",
    "covid_cancer_6":"Can patients with cancer on clinical trials receive the COVID-19 vaccine?",
    "covid_cancer_7":"if my antibody test shows the low antibody level, do I need an additional vaccine dose?",
    "covid_pregnancy_1":"Can pregnant women receive COVID-19 vaccines?",
    "covid_pregnancy_2":"How does COVID-19 affect pregnant women and their babies?",
    "covid_pregnancy_3":"Are COVID-19 vaccines during pregnancy effective?",
    "covid_pregnancy_4":"Can women who are trying to become pregnant receive COVID-19 vaccines?",
    "covid_pregnancy_5":"are side effects from the Johnson & Johnson (Janssen) vaccine during pregnancy?",
    "covid_pregnancy_6":"Will the COVID-19 vaccine benefit my kid if I choose to get vaccinated during my pregnancy?",
    "covid_pregnancy_7":"I am breastfeeding. Should I get vaccinated?",
    "covid_pregnancy_8":"Will the vaccine affect menstrual periods?",
    "covid_pregnancy_9":"Will getting vaccinated affect my chance of getting pregnant in the future??",
    "covid_pregnancy_10":"do I need a booster prior to pregnancy",
    "covid_lung_disease_1":"Do patients with lung disease have covid complications?",
    "covid_lung_disease_2":"Should I get vaccinated if I have lung disease? ",
    "covid_lung_disease_3":"What should lung disease patients do If they have symptoms of COVID-19?",
    "covid_lung_disease_4":"Should i Keep taking my prescribed medications if i have suspected covid?",
    "covid_lung_disease_5":"Do lung disease patients more likely to get covid?",
    "covid_lung_disease_6":"Are there additional measures for lung disease people to avoid getting covid?",
    "covid_lung_disease_7":"Can I increase my normal dosage of treatments to protect myself from COVID-19?",
    "covid_lung_disease_8":"What should lung disease patients do if they get covid?",
    "covid_old_people_1":"What older people should do to stop covid from spreading",
    "covid_old_people_2":"COVID-19 Community Helpline for older people",
    "covid_old_people_3":"What should older people do if they have a symptoms or exposure",
    "covid_old_people_4":"How can older people manage their health?",
    "covid_old_people_5":"Are older people at high risk of getting COVID-19",
    "covid_old_people_6":"Does aspirin make COVID-19 worse?",
    "covid_old_people_7":"What if elderly use hydroxychloroquine on a regular basis but can't obtain a refill since it's being used for COVID-19?",
    "covid_old_people_8":"What should older people do if they have dental issues",
   }
TEST_INTENT = {
    "covid_test_1":"What kinds of test are available?",
    "covid_test_4":"How to do an antigen test?",
    "covid_test_11":"How to get a covid-19 recovery certificate",
    "covid_test_14":"What is PCR test?",
    "covid_test_2":"What is antigen test?",
    "covid_test_3":"When can I do PCR test?",
    "covid_test_5":"When can I do an antigen test?",
    "covid_test_6":"How to book an antigen test?",
    "covid_test_7":"Do children need an antigen test?",
    "covid_test_8":"How to do an antigen test with children",
}
SYMPTOM_INTENT = {
    "covid_symptom_1":"What are the most common symptom of covid",
    "covid_symptom_7":"What should I do if I have a high fever from covid",
    "covid_symptom_10":"What should I do if I get dehydration from covid",
    "covid_symptom_19":"Symptoms for fatigue",
    "covid_symptom_12":"Symptoms of dehydration",
    "covid_symptom_16":"Children have a serious dehydration from covid",
    "covid_symptom_17":"The symptoms of dehydration in babies and children",
    "covid_symptom_18":"Lower the risk of dehydration for children",
}
TREATMENT_INTENT = {
    "covid_treatment_1":"The way to deal with covid at home ",
    "covid_treatment_2":"What can I take to treat my symptoms",
    "covid_treatment_3":"Does antibiotics work to covid symptoms",
    "covid_treatment_4":"Is ibuprofen good for covid symptoms",
    "covid_treatment_5":"How do I take care of my cough?",
    "covid_treatment_6":"What should I do if I have asthma health condition",
    "covid_treatment_7":"What should I do if I have shortness of breath",
    "covid_treatment_8":"What should I do if I lose my smell from covid",
    "covid_treatment_9":"More about Anti-inflammatory medicines"
}
OTHER_INTENT = {
    "covid_other_1": "What is COVID-19",
    "covid_other_2": "Who should get a COVID test",
    "covid_other_3": "what should I do if I start to feel unwell"
}
ISOLATION_INTENT = {
    "covid_isolation_1":"Why I need to do self-quarantine",
    "covid_isolation_2":"When I need to do self-quarantine",
    "covid_isolation_3":"What should I do for self-quarantine",
    "covid_isolation_4":"What I should not do in self-isolation",
    "covid_isolation_5":"How long do I need to do self-quarantine",
    "covid_isolation_6":"What should I do after 7 days of self-isolation",
    "covid_isolation_7":"When do my children need to quarantine",
    "covid_isolation_8":"How long does it take for children isolation",
    "covid_isolation_9":"How to deal with self-isolation"
}
RISK_INTENT = {
    "covid_risk_1":"Who are in the higher risk from covid-19",
    "covid_risk_2":"Who are in the very high risk",
    "covid_risk_3":"More Information for high risk groups",
    "covid_risk_4":"More Information for very high risk groups"
}
VACCINE_INTENT = {
    "covid_vaccine_1":"What is COVID-19 vaccine",
    "covid_vaccine_4":"How many vaccine do I need for first round",
    "covid_vaccine_7":"Why is it important to get the covid vaccine?",
    "covid_vaccine_15":"Is the vaccine safe",
    "covid_vaccine_17":"What are the side effects of the vaccine",
    "covid_vaccine_18":"What might happen in the few days if I get the vaccine",
    "covid_vaccine_19":"Why I get a fever after I take the vaccine",
    "covid_vaccine_20":"How long will the vaccine work",
    "covid_vaccine_21":"Does the vaccine work in everyone",
    "covid_vaccine_22":"Will I spread covid to others if I get the vaccine",
    "covid_vaccine_23":"How long does the Nuvaxovid vaccine last",
    "covid_vaccine_24":"Is the vaccine effective for children aged 5 to 11 years",
    "covid_vaccine_25":"Is the vaccine safe for children",
    "covid_vaccine_26":"How to get a covid vaccine",
    "covid_vaccine_27":"what is mRNA vaccine",
    "covid_vaccine_28":"more vaccine information for pregnant women",
    "covid_vaccine_29":"Recommended vaccines for pregnant women",
    "covid_vaccine_30":"More information for vaccine safety",
    "covid_vaccine_31":"Uncommon side effects of the vaccine",
    "covid_vaccine_32":"More information for vaccine side effects"
}
QUESTION_TYPES = {
    "covid test":"covid test",
    "covid symptoms":"covid symptoms",
    "covid treatment":"covid treatment",
    "covid self-isolation":"covid self-isolation",
    "covid risk":"covid risk",
    "covid vaccine":"covid vaccine",
    "other":"other"
}

TEST = [{
                "title": list(TEST_INTENT.values())[i],
                "payload": "/{}".format(list(TEST_INTENT.keys())[i])
                }for i in range(5)
                ]
SYMPTOM = [{
                "title": list(SYMPTOM_INTENT.values())[i],
                "payload": "/{}".format(list(SYMPTOM_INTENT.keys())[i])
                }for i in range(5)
                ]

TREATMENT = [{
                "title": list(TREATMENT_INTENT.values())[i],
                "payload": "/{}".format(list(TREATMENT_INTENT.keys())[i])
                }for i in range(5)
                ]

ISOLATION = [{
                "title": list(ISOLATION_INTENT.values())[i],
                "payload": "/{}".format(list(ISOLATION_INTENT.keys())[i])
                }for i in range(5)
                ]
RISK = [{
                "title": list(RISK_INTENT.values())[i],
                "payload": "/{}".format(list(RISK_INTENT.keys())[i])
                }for i in range(len(RISK_INTENT))
                ]
VACCINE = [{
                "title": list(VACCINE_INTENT.values())[i],
                "payload": "/{}".format(list(VACCINE_INTENT.keys())[i])
                }for i in range(5)
                ]
OTHER = [{
                "title": list(OTHER_INTENT.values())[i],
                "payload": "/{}".format(list(OTHER_INTENT.keys())[i])
                }for i in range(len(OTHER_INTENT))
                ]
NAME_PAIR = {
"Victoria":"female",
"Hannah":"female",
"Addison":"female",
"Paul":"male",
"Leah":"female",
"Lucy":"female",
"Steven":"male",
"Eliana":"female",
"Ivy":"female",
"Everly":"female",
"Lillian":"female",
"John":"male",
"Paisley":"female",
"Elena":"female",
"Naomi":"female",
"Maya":"female",
"Robert":"male",
"Andrew":"male",
}
NAME_LIST = [
"Victoria",
"Hannah",
"Addison",
"Paul",
"Leah",
"Lucy",
"Steven",
"Eliana",
"Ivy",
"Everly",
"Lillian",
"John",
"Paisley",
"Elena",
"Naomi",
"Maya",
"Robert",
"Andrew"
]
NAME = [
"* Victoria \n",
"* Hannah \n",
"* Addison \n",
"* Paul \n",
"* Leah \n",
"* Lucy \n",
"* Steven \n",
"* Eliana \n",
"* Ivy \n",
"* Everly \n",
"* Lillian \n",
"* John \n",
"* Paisley \n",
"* Elena \n",
"* Naomi \n",
"* Maya \n",
"* Robert \n",
"* Andrew \n"
]
CONDIT = [
"diabetes",
"kidney disease",
"immunodeficiency",
"cancer",
"lung disease",
"none"
]

DIABETES_INTENT = {
    "covid_diabetes_1":"Are people with diabetes more likely to get COVID-19?",
    "covid_diabetes_4":"Does COVID-19 cause diabetes?",
    "covid_diabetes_3":"Do persons with type 1 and type 2 diabetes meet different risks?",
    "covid_diabetes_5":"What should diabetics do if they feel they are developing covid symptoms?",
}
DIABETES_BUTTON = [{
                "title": list(DIABETES_INTENT.values())[i],
                "payload": "/{}".format(list(DIABETES_INTENT.keys())[i])
                }for i in range(len(DIABETES_INTENT))
                ]
KIDNEY_INTENT = {
    "covid_kidney_1":"Is the COVID-19 vaccine safe for patients with kidney disease",
    "covid_kidney_2":"Are people with Chronic Kidney Disease at higher risk of complications?",
    "covid_kidney_4":"Does the COVID-19 vaccine affect the kidneys?",
}
KIDNEY_BUTTON = [{
                "title": list(KIDNEY_INTENT.values())[i],
                "payload": "/{}".format(list(KIDNEY_INTENT.keys())[i])
                }for i in range(len(KIDNEY_INTENT))
                ]

CANCER_INTENT = {
    "covid_cancer_1": "Is it safe to get the COVID-19 vaccine while receiving cancer treatment?",
    "covid_cancer_6": "Can patients with cancer on clinical trials receive the COVID-19 vaccine?",
    "covid_cancer_7": "if my antibody test shows the low antibody level, do I need an additional vaccine dose?",
}
CANCER_BUTTON = [{
                "title": list(CANCER_INTENT.values())[i],
                "payload": "/{}".format(list(CANCER_INTENT.keys())[i])
                }for i in range(len(CANCER_INTENT))
                ]
IMMU_INTENT = {
    "covid_immunodeficiency_1": "Are COVID-19 vaccines safe for people with immunodeficiency?",
    "covid_immunodeficiency_3": "What precautions should people with immunodeficiencies take?",
    "covid_immunodeficiency_6": "Which of the COVID vaccines is best for people with primary and secondary immunodeficiency?",
}
IMMU_BUTTON = [{
                "title": list(IMMU_INTENT.values())[i],
                "payload": "/{}".format(list(IMMU_INTENT.keys())[i])
                }for i in range(len(IMMU_INTENT))
                ]

PREG_INTENT = {
    "covid_pregnancy_1":"Can pregnant women receive COVID-19 vaccines?",
    "covid_pregnancy_2":"How does COVID-19 affect pregnant women and their babies?",
    "covid_pregnancy_7":"I am breastfeeding. Should I get vaccinated?",

}
PREG_BUTTON = [{
                "title": list(PREG_INTENT.values())[i],
                "payload": "/{}".format(list(PREG_INTENT.keys())[i])
                }for i in range(len(PREG_INTENT))
                ]

LUNG_INTENT = {
    "covid_lung_disease_1":"Do patients with lung disease have covid complications?",
    "covid_lung_disease_2":"Should I get vaccinated if I have lung disease? ",
    "covid_lung_disease_8":"What should lung disease patients do if they get covid?",
}
LUNG_BUTTON = [{
                "title": list(LUNG_INTENT.values())[i],
                "payload": "/{}".format(list(LUNG_INTENT.keys())[i])
                }for i in range(len(LUNG_INTENT))
                ]

OLD_INTENT = {
    "covid_old_people_1":"What older people should do to stop covid from spreading",
    "covid_old_people_3":"What older people should do to stop covid from spreading",
    "covid_old_people_5":"What older people should do to stop covid from spreading",
}
OLD_BUTTON = [{
                "title": list(OLD_INTENT.values())[i],
                "payload": "/{}".format(list(OLD_INTENT.keys())[i])
                }for i in range(len(OLD_INTENT))
                ]