#include <iostream>
#include <unordered_set>
#include <string>
#include <algorithm>
#include "cppjieba/Jieba.hpp"

using namespace std;
using namespace cppjieba;

const char* const DICT_PATH = "../dict/jieba.dict.utf8";
const char* const HMM_PATH = "../dict/hmm_model.utf8";
const char* const USER_DICT_PATH = "../dict/user.dict.utf8";
const char* const IDF_PATH = "../dict/idf.utf8";
const char* const STOP_WORD_PATH = "../dict/stop_words.utf8";

void stringToLower(string &s) {
  std::transform(s.begin(), s.end(), s.begin(), ::tolower);
}

bool loadUserWordDict(const string& filePath, Jieba &jieba) {
  ifstream ifs(filePath.c_str());
  if(!ifs.is_open()) return false;
  string word;
  while (getline(ifs, word)) {
    if(word.length()==0) continue;
    jieba.InsertUserWord(word);
  }
  return true;
}

bool loadStopWordDict(const string& filePath, unordered_set<string> &stopWords) {
  ifstream ifs(filePath.c_str());
  if(!ifs.is_open()) return false;
  string line;
  while (getline(ifs, line)) {
    stopWords.insert(line);
  }
  return true;
}

bool isDigits(string &s) {
  return s.find_first_not_of("0123456789.") == std::string::npos;
}

int cutWords(Jieba &jieba, unordered_set<string> &stopWords, string &s, vector<string> &words) {
  if(s.empty()) return -1;
  vector<string> candidateWords;
  jieba.Cut(s, candidateWords, true);
  size_t n = candidateWords.size();
  for(size_t i=0; i<n; i++) {
    if(candidateWords[i] == "." || candidateWords[i] == " ") continue;
    stringToLower(candidateWords[i]);
    if(isDigits(candidateWords[i])) candidateWords[i] = "NUM";
    if(stopWords.find(candidateWords[i]) == stopWords.end()) words.push_back(candidateWords[i]);
  }
  return 0;
}

int cutWordsWithTag(Jieba &jieba, string &s, vector<string> &words, unordered_set<string> &filterTags) {
  if(s.empty()) return -1;
  vector<pair<string, string>> tagres;
  jieba.Tag(s, tagres);
  int n = tagres.size();
  for(int i=0; i<n; i++) {
    // cout << tagres[i].first << " " << tagres[i].second << endl;
    if(isDigits(tagres[i].first)) {
      words.push_back("NUM");
      continue;
    }
    if(filterTags.find(tagres[i].second) != filterTags.end()) words.push_back(tagres[i].first);
  }
  return 0;
}

void joinWords(vector<string> &words, string &delimiter, string &result) {
  result = limonp::Join(words.begin(), words.end(), delimiter);
} 

int main(int argc, char** argv) {
  cppjieba::Jieba jieba(DICT_PATH,
        HMM_PATH,
        USER_DICT_PATH,
        IDF_PATH,
        STOP_WORD_PATH);
  vector<string> words;
  string s;
  string result;
  string delimiter = " ";

  // unordered_set<string> filterTags = {"rr", "d", "p", "u", "c", "e", "y", "w", "m"};
  unordered_set<string> filterTags = {"ns"};
  unordered_set<string> stopWords;
  
  loadStopWordDict(STOP_WORD_PATH, stopWords);
  loadUserWordDict(USER_DICT_PATH, jieba);

  for(; getline(cin, s); ) {
    words.clear();
    result.clear();
    // cutWordsWithTag(jieba, s, words, filterTags);
    cutWords(jieba, stopWords, s ,words);
    joinWords(words, delimiter, result);
    cout << s << "\t" << result << endl;
  }

  return EXIT_SUCCESS;
}
