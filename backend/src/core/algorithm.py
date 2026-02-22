import math
from typing import List, Dict, Any, Optional
from collections import defaultdict


class AkinatorLogic:

    def __init__(self,
                 characters: List[Dict[str, Any]],
                 questions: List[Dict[str, Any]],
                 matrix: Dict[tuple, int]):

        self.characters = characters
        self.questions = questions
        self.matrix = matrix


        self.answer_mapping = {
            'yes': 4,
            'probably': 3,
            'dont_know': 2,
            'probably_not': 1,
            'no': 0
        }



    def _calculate_entropy(self, weights: Dict[int, float]) -> float:

        total = sum(weights.values())

        if total == 0:
            return 0.0

        entropy = 0.0
        for weight in weights.values():
            if weight > 0:
                p = weight / total
                entropy -= p * math.log2(p)

        return entropy

    def _get_character_score(self,
                             char_id: int,
                             question_id: int) -> int:

        return self.matrix.get((char_id, question_id), 2)

    def _calculate_information_gain(self,
                                    weights: Dict[int, float],
                                    question_id: int,
                                    asked_questions: List[int]) -> float:

        if question_id in asked_questions:
            return 0.0

        current_entropy = self._calculate_entropy(weights)

        if current_entropy == 0:
            return 0.0

        splits = defaultdict(dict)

        for char_id, weight in weights.items():
            score = self._get_character_score(char_id, question_id)
            splits[score][char_id] = weight

        total_weight = sum(weights.values())
        weighted_entropy = 0.0

        for score, split_weights in splits.items():
            split_total = sum(split_weights.values())
            proportion = split_total / total_weight
            split_entropy = self._calculate_entropy(split_weights)
            weighted_entropy += proportion * split_entropy

        ig = current_entropy - weighted_entropy
        return ig

    def _choose_best_question(self,
                              weights: Dict[int, float],
                              asked_questions: List[int]) -> Optional[int]:

        best_question = None
        max_ig = -1

        for question in self.questions:
            q_id = question['id']

            if q_id in asked_questions:
                continue

            ig = self._calculate_information_gain(weights, q_id, asked_questions)

            if ig > max_ig:
                max_ig = ig
                best_question = q_id

        return best_question

    def _update_weights(self,
                        weights: Dict[int, float],
                        question_id: int,
                        user_answer: int) -> Dict[int, float]:

        new_weights = {}

        for char_id, weight in weights.items():
            char_score = self._get_character_score(char_id, question_id)

            difference = abs(user_answer - char_score)


            multipliers = {
                0: 2.0,
                1: 1.5,
                2: 1.0,
                3: 0.5,
                4: 0.2
            }

            multiplier = multipliers[difference]
            new_weight = weight * multiplier

            if new_weight > 0.01:
                new_weights[char_id] = new_weight

        return new_weights


    def get_start_question_id(self) -> int:
        weights = {char['id']: 1.0 for char in self.characters}

        best_q = self._choose_best_question(weights, asked_questions=[])

        if best_q is None:
            return self.questions[0]['id']

        return best_q

    def get_next_step(self,
                      user_history: List[Dict[str, Any]],
                      threshold: float = 0.8) -> Dict[str, Any]:
        weights = {char['id']: 1.0 for char in self.characters}
        asked_questions = []

        for entry in user_history:
            question_id = entry['question_id']
            answer_str = entry['answer']

            user_answer = self.answer_mapping.get(answer_str, 2)

            weights = self._update_weights(weights, question_id, user_answer)
            asked_questions.append(question_id)

        if not weights:
            return {
                'type': 'guess',
                'character_id': self.characters[0]['id'],
                'probability': 0.0
            }

        total_weight = sum(weights.values())

        best_char_id = max(weights, key=weights.get)
        best_weight = weights[best_char_id]
        probability = best_weight / total_weight

        if probability >= threshold:
            return {
                'type': 'guess',
                'character_id': best_char_id,
                'probability': probability
            }

        next_question = self._choose_best_question(weights, asked_questions)

        if next_question is None:
            return {
                'type': 'guess',
                'character_id': best_char_id,
                'probability': probability
            }

        current_entropy = self._calculate_entropy(weights)

        return {
            'type': 'question',
            'question_id': next_question,
            'entropy': current_entropy
        }
