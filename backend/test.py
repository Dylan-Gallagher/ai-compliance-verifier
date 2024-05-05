# To run - 'python3 test.py'

import unittest
from auto_label_function import better_studio, paragraph_to_labeled_sentences, get_character_index, punc_split


class TestParagraphToLabeledSentences(unittest.TestCase):
    # This function is to test paragraph_to_labeled_sentences used in better_studio

    # PASS 
    # Note - empty sentence is added to the sentence count, which increases the sentence count

    def test_complex_paragraph_processing(self):
        paragraph = (
            "Biometric categorisation systems that are based on individuals’ biometric data, "
            "such as an individual person’s face or fingerprint, to deduce or infer an individuals’ political opinions, "
            "trade union membership, religious or philosophical beliefs, race, sex life or sexual "
            "orientation should be prohibited. This prohibition does not cover the lawful labelling, "
            "filtering or categorisation of biometric datasets acquired in line with Union or national law "
            "according to biometric data, such as the sorting of images according to hair colour or eye "
            "colour, which can for example be used in the area of law enforcement."
        )
        
        tokens_list, tags_list, sentences = paragraph_to_labeled_sentences(paragraph)
        
        expected_number_of_sentences = 3 # Should be 2 as there are 2 sentences in the paragraph 
        self.assertEqual(len(sentences), expected_number_of_sentences, "The paragraph was not split into the correct number of sentences.")
        
        for tokens, tags in zip(tokens_list, tags_list):
            self.assertIsInstance(tokens, list, "Tokens for a sentence should be in a list.")
            self.assertIsInstance(tags, list, "Tags for a sentence should be in a list.")
            self.assertEqual(len(tokens), len(tags), "Each token should have a corresponding tag.")

class TestBetterStudio(unittest.TestCase):
    #This function is to test the output of better_studio 

    # FAIL - When getting the start index for entity. 
    # Note - It is able to get the labels and the text ie SYS + PER and Ai system + natural persons

    def test_better_studio(self):

        # Example sentence 1
        tokens_list = [["AI", "systems", "providing", "social", "scoring", "of", "natural", "persons", "by", "public", "or", "private", "actors", "may", "lead", "to", "discriminatory", "outcomes", "and", "the", "exclusion", "of", "certain", "groups"]]
        tag_lists = [["B-SYS", "I-SYS", "O", "O", "O", "O", "B-PER", "I-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]]
        sentences = ["AI systems providing social scoring of natural persons by public or private actors may lead to discriminatory outcomes and the exclusion of certain groups."]
        
        expected_labels = ["SYS", "PER"]
        expected_texts = ["AI systems", "natural persons"]

        expected_starts = [0, 39]
        expected_ends = [10, 54]

         # Example sentence 2
        # tokens_list = [["Technical", "inaccuracies", "of", "AI", "systems", "intended", "for", "the", "remote", "biometric", "identification", "of", "natural", "persons", "can", "lead", "to", "biased", "results", "and", "entail", "discriminatory", "effects."]]
        # tag_lists = [["O", "O", "O", "B-SYS", "I-SYS", "O", "O", "O", "O", "B-ALG", "I-ALG", "O", "B-PER", "I-PER", "O", "O", "O", "O", "O", "O", "O", "O", "O"]]
        # sentences = ["Technical inaccuracies of AI systems intended for the remote biometric identification of natural persons can lead to biased results and entail discriminatory effects."]

        # expected_labels = ["SYS", "ALG", "PER"]
        # expected_texts = ["AI systems", "biometric identification", "natural persons"]

        # expected_starts = [27, 54, 77]  
        # expected_ends = [35, 75, 90] 

        output = better_studio(tokens_list, tag_lists, sentences)

        labels = len(output[0]['predictions'][0]['result'])

        self.assertEqual(len(output[0]['predictions'][0]['result']), len(expected_labels), "Number of entities predicted does not match expected.")

        for idx, label in enumerate(expected_labels):
            result = output[0]['predictions'][0]['result'][idx]
            self.assertIn(label, result['value']['labels'], f"Entity '{expected_texts[idx]}' with label '{label}' not found.")
            self.assertEqual(result['value']['text'], expected_texts[idx], f"Text for entity '{label}' does not match.")
            self.assertEqual(result['value']['start'], expected_starts[idx], f"Start index for entity '{label}' does not match.")
            self.assertEqual(result['value']['end'], expected_ends[idx], f"End index for entity '{label}' does not match.")
class TestGetCharacterIndex(unittest.TestCase):
    # This function is to test get_character_index within the better_studio

    # FAIL - At 2019 (actual output = 128) and fails at HLEG is not in the sentence
    # Note - After debugging, the index discrincimes if there are characters that are non alphabetic such as , ( ) etc. 

    def test_sentence_indices(self):
        sentence = "While the risk-based approach is the basis for a proportionate and effective set of binding rules, it is important to recall the 2019 Ethics Guidelines for Trustworthy AI developed by the independent High-Level Expert Group on AI (HLEG) appointed by the Commission."
        word_list = sentence.split()
        for token in word_list:
            word_list = punc_split(token, word_list, word_list.index(token), 0, 0)
        tests = [
            ("While", 0),
            ("proportionate", 49),
            ("2019", 129),
            ("HLEG", 231)  
        ]

        for word, expected_index in tests:
            with self.subTest(word=word):
                actual_index = get_character_index(word_list, word_list.index(word))
                self.assertEqual(actual_index, expected_index, f"Index for '{word}' did not match expected value.")


if __name__ == '__main__':
    unittest.main()
