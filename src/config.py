#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/opcut.
#   Use MznStrouhal@gmail.com to contact the author.


import xml.etree.ElementTree as et
import os
from typing import Dict, List, Tuple
import dataclasses
import appdirs
import shutil


APP_NAME = "OpCut"
AUTHOR_NAME = "OpCut"
LOCAL_DATA_FOLDER = appdirs.user_data_dir(APP_NAME, AUTHOR_NAME)
CONFIG_FILE_NAME = "config.xml"
CONFIG_FILE_PATH = os.path.join(LOCAL_DATA_FOLDER,CONFIG_FILE_NAME)


class MissingWordInTranslation(Exception): pass
class NoValidTranslationForApplication(Exception): pass
class XML_DoesNotValidateAgainst(Warning): pass


try: 
    app_config = et.parse(CONFIG_FILE_PATH)
except:
    if not os.path.isdir(LOCAL_DATA_FOLDER): os.makedirs(LOCAL_DATA_FOLDER)
    shutil.copyfile("src/config.xml",CONFIG_FILE_PATH)
    app_config = et.parse(CONFIG_FILE_PATH)


localization = app_config.getroot().find("Localization")
if localization is not None: loc_path = localization.attrib["LangDirectory"]

#store only lang files
lang_files:Dict[str,et.ElementTree] = dict()
file_names:List[str] = os.listdir(loc_path)
file_names.sort()


import warnings
for file_name in os.listdir(loc_path):
    if not file_name.endswith(".xml"): continue
    try: 
        file = et.parse(loc_path+file_name)
        if file.getroot().tag=="Language":
            lang_files[file_name.removesuffix(".xml")] = file
    except:
        warnings.warn("Some files in 'localization' do not validate against schema.", UserWarning)


if len(lang_files)==0: raise NoValidTranslationForApplication(
    "No language provided for the application. "
    "Place a valid language file into localization folder."
)


DEFAULT_LANGUAGE = "es_us"
lang_name = localization.find("Language").text
lang_file_schema_path = loc_path+"lang.xsd"
lang_file_path = loc_path+lang_name+".xml"
file_names = [localization.find("Language").text, DEFAULT_LANGUAGE] + file_names
SESSION_LANGUAGE = "No language available"
for name in file_names:
    path = loc_path+name+".xml"
    if os.path.isfile(lang_file_path):
        SESSION_LANGUAGE = et.parse(loc_path+lang_name+".xml").getroot()

if SESSION_LANGUAGE=="No language available": raise NoValidTranslationForApplication(
    "None of the files in 'localization' directory provides valid translation."
)


def wtext(item_id:str,*parents:str)->str:
    parent = SESSION_LANGUAGE
    for p in parents: parent = parent.find(p)
    item = parent.find(item_id)
    if item==None: raise MissingWordInTranslation(
        f"The string {item_id} is not defined in any language file in 'localization'."
    )
    return parent.find(item_id).attrib["Text"]


@dataclasses.dataclass(frozen=True)
class WLink: 
    label:str
    link:str

def wlink(item_id:str,*parents:str)->WLink:
    parent = SESSION_LANGUAGE
    for p in parents: parent = parent.find(p)
    item = parent.find(item_id)
    if item==None: raise MissingWordInTranslation(
        f"The string {item_id} is not defined in any language file in 'localization'."
    )
    return WLink(parent.find(item_id).attrib["Label"], parent.find(item_id).attrib["Link"])

#bind language names to changes in the config file
LANGUAGE_OPTIONS = dict()
for l in lang_files:
    LANGUAGE_OPTIONS[lang_files[l].getroot().attrib["Id"]] = lang_files[l].getroot().attrib["Name"]

def set_lang(language_id:str):
    localization.find("Language").text = language_id
    app_config.write(CONFIG_FILE_PATH)

def language_change_notification(language_id:str)->Tuple[str,str]:
    return \
        lang_files[language_id].find("ApplicationFrame").find("language_change_notification_title").attrib["Text"],\
        lang_files[language_id].find("ApplicationFrame").find("language_change_notification").attrib["Text"]