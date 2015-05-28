import logging
import sys
from t2db_objects.parameters import generate_parameters
from t2db_objects.parameters import generate_config
from t2db_objects.logger import setup_logging

from clean_text.cleaner import cleaner 

logger = logging.getLogger('clean_text')

conf_fields = [
  {'name':'over_write_output_file','kind':'non-mandatory','type':bool,'default':False},
  {'name':'buffer_size','kind':'non-mandatory','type':int,'default':100},
  {'name':'split_criteria_line','kind':'non-mandatory','type':str, 'default':'\t'},
  {'name':'stopword_file_path','kind':'non-mandatory','type':str,'default':'stopwords'},
  {'name':'sentence_proc_list','kind':'mandatory','type':list,'default':None},
  {'name':'token_proc_list','kind':'mandatory','type':list,'default':None},
  {'name':'fields','kind':'mandatory','type':list,'default':None},
  {'name':'text_field','kind':'mandatory','type':str,'default':None},
  {'name':'new_fields','kind':'mandatory','type':list,'default':None},
  {'name':'new_text_field','kind':'mandatory','type':str,'default':None},
]

param_fields = [
  {'name':'input_file','kind':'mandatory','type':str,'default':None,'abbr':'-f','help':'Input file'},
  {'name':'output_file','kind':'mandatory','type':str,'default':None,'abbr':'-o','help':'Output file'},
  {'name':'config_file','kind':'non-mandatory','type':str,'default':None, 'abbr':'--config','help':'Configuration file'},
]

def run_cleaner():
  """ Runnable function
  """
  setup_logging()
  description = 'Text cleaner'
  epilog = 'Pablo Torres, pablo.torres.t@gmail.com'
  params = generate_parameter(param_fields, description, epilog)
  config = generate_config(conf_fields, params.config_file)
  cleaner(params, config)
  sys.exit(0)

