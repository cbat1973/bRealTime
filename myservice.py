#!/usr/bin/python

from bottle import Bottle, request, response
from datetime import datetime
from functools import wraps
import logging, urllib, numpy

logger = logging.getLogger('app')

# set up the logger
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_to_logger(fn):
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        # modify this to log exactly what you need:
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response
    return _log_to_logger

app = Bottle()
app.install(log_to_logger)

def answers_func(quest):

    info={  	
        'Years':'5',
 	'Phone':'773-454-4243',
 	'Source':'https://github.com/cbat1973/bRealTime.git',
 	'Name':'Marvin N. Germany ',
 	'Email Address':'cbat1973@gmail.com',
 	'Resume':'https://github.com/cbat1973/bRealTime.git',
 	'Degree':'Masters of Information Systems Public Policy and Management Carnegie Mellon University 1997',
 	'Position':'DevOps Manager/Engineer',
 	'Referrer':'Jenny Gasparis',
	'Status':'Yes'
} 

    answer=info[quest]
    return answer
 	    
def puzzle_func():
        x=request.url.split('+')[4:7]
        #### convert x to a string ####
        x=''.join(x)
        puzzle_string = urllib.unquote(x).decode('utf8')        

        puzzle_list = puzzle_string.splitlines()

        ## Adding an additional element to complete 
        puzzle_list[0] = 'XABCD'

        ca = numpy.chararray((5,5))
        for i in range(0,5):
            tmp_array = list(puzzle_list[i])
            #print tmp_array
            for j in range(0,5):
                #ca[i,j] = puzzle_list[j]
                ca[i,j] = tmp_array[j]
                
        ### Initialize the special columns i.e [A,A], [B,B] etc...
        for i in range(1,5): 
            if ca[i,i] != '=':
                ca[i,i] ='0'

        ### Find the "seed" column
        for i in range(0,5):
            for j in range(0,5): 
                if ca[i,j] == '=':    
                    col = j
                    
       ### Find the "seed" row
        for i in range(1,5):
            if ca[i,col] == '-':
                    row = i
                    
        #### Init tnd update the "seed" column
        count = 1
        while (count < 5):
            if ca[row, count] != '-' and ca[row,count] != '0':
                    ca_update = ca[row,count]
                    ca[row,col] = ca_update
            count = count + 1

        ###### Do the inverse 

        for i in range(1,5):
            for j in range(1,5):
                if ca[i,j] == '0':
                     ca[i,j] = '='
                elif ca[i,j] == '<':
                     ca[j,i] = '>'
                elif ca [i,j] == '>':
                     ca[j,i] = '<'

        

        for i in range(1,5):
           score = 0
           count = 0
           for j in range(1,5):
                if ca[i,j] == '>':
                    score = score + 1
                    count = count + 1
                elif ca[i,j] == '<':
                    score = score - 1
                    count = count + 1
                elif ca[i,j] == '=':
                    count = count + 1
                    
           if (count >= 3):
                if score == 2:
                   for z in range(1,5):
                        if (i != z):
                            ca[i,z]='>'
           else:
               for z in range(1,5):
                        if (i != z):
                            ca[i,z]='<' 

### Final Inverse

           for i in range(1,5):
            for j in range(1,5):
                if (i != j):
                    if ca[i,j] == '<':
                        ca[j,i] = '>'
                elif ca [i,j] == '>':
                     ca[j,i] = '<'
        
        

        string1 = ''.join(ca[0])
        string1 = 'ABCD'
        string2 = ''.join(ca[1])
        string3 = ''.join(ca[2])
        string4 = ''.join(ca[3])
        string5 = ''.join(ca[4])


        #### Merge the strings 
        
        ns = (string1 + '\n' + string2 + '\n' + string3 + '\n' + string4 + '\n' + string5 + '\n')
        return[ns]
        ### End function 


@app.route('/')
def home():
    q = request.query['q']
    d = request.query['d']

    if q == 'Puzzle':
        pr=puzzle_func()
        return(pr)
    elif q == 'Ping':
        return['OK']
    else:    
        result=answers_func(q)
        return result
app.run(host='0.0.0.0', port='8080', quiet=True)
