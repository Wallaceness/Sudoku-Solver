#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import Sudoku

def mapping(dictionary):#This initializes the dictionary used for the string
    for number in range(1,82):#substitution to all '' to start.
        dictionary[str(number)]=''
    dictionary['error']=''
    dictionary['quantity']=''
    dictionary['q_error']=''
    

class MainHandler(webapp2.RequestHandler):
    def solve_(self, solve, subs):
        #Class method used to handle all solve requests.
        if solve:
            sudoku=[]
            for number in Sudoku.boxes:#Uses the box list from Sudoku module to
                n=self.request.get(str(number+1))#create an accurate conversion from html table to the solver function.
                if n not in ['1','2','3','4','5','6','7','8','9','']:
                    subs['error']="Invalid sudoku"#Checks sudoku
                    return
                if n:
                    sudoku.append(int(n))
                else:
                    sudoku.append('')
            try:
                result=Sudoku.solver(sudoku)
            except ValueError:#This is a more complex check to see if a puzzle was
                subs['error']="Invalid sudoku"#not solvable even though it was
                return#not immediately apparent.
            if result=="Invalid sudoku":
                subs['error']="Invalid sudoku"
                return
            for number in range(0,81):#And this reconverts the sudoku back to it's original format
                subs[str(number+1)]=result[Sudoku.boxes[number]]#from the python list and assigns appropriate values to mapping dict.
    def generate_(self, generate, subs):
        if generate:#Handles all generate request.
            quantity=self.request.get("quantity")
            if not quantity.isdigit() or quantity<0:#Makes sure valid quantity is entered.
                subs["q_error"]="Invalid quantity"
                return
            response=Sudoku.generate(quantity)
            for number in range(0,81):#Converts from python list to table format.
                subs[str(number+1)]=response[Sudoku.boxes[number]]
    def get(self):
        table=open("table.html").read()#The source for the html.
        subs={}
        mapping(subs)
        self.response.write(table%subs)
    def post(self):
        table=open("table.html").read()
        subs={}
        mapping(subs)
        solve=self.request.get("solve")
        generate=self.request.get("generate")
        MainHandler.solve_(self, solve, subs)
        MainHandler.generate_(self, generate, subs)
        self.response.write(table%subs)
#That's it!

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
