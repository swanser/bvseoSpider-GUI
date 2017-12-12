#bvseoSpider-GUI v0.02A
#SMW

import tkinter, requests, bs4
from tkinter import filedialog, messagebox, ttk


class bvSEOFrame(tkinter.Frame):

    def __init__(self, parent):

        tkinter.Frame.__init__(self, parent)
        self.generateWidgets()
        

    def generateWidgets(self):

        #Target Frame
        self.targetFrame = tkinter.Frame(self, bd = 2, relief = 'sunken')
        self.targetFrame.targetLabel = tkinter.Label(self.targetFrame, text = 'Target:')
        self.targetFrame.targetVariable = tkinter.StringVar()
        self.targetFrame.targetEntry = ttk.Combobox(self.targetFrame, textvariable = self.targetFrame.targetVariable, width = 76)
        self.targetFrame.targetSubmitButton = tkinter.Button(self.targetFrame, text = 'Launch!', command = self.scrape)
        self.targetFrame.targetLabel.grid(row = 0, column = 0)
        self.targetFrame.targetEntry.grid(row = 0, column = 1)
        self.targetFrame.targetSubmitButton.grid(row = 0, column = 2)

        #Target Detail Frame
        self.targetDetailFrame = tkinter.LabelFrame(self, bd = 2, relief = 'sunken', text = 'Target Detail:')
        self.targetDetailFrame.productDetectedLabel = tkinter.Label(self.targetDetailFrame, text = 'Product Detected:')
        self.targetDetailFrame.productDetectedVariable = tkinter.StringVar()
        self.targetDetailFrame.productDetectedDisplay = tkinter.Label(self.targetDetailFrame, textvariable = self.targetDetailFrame.productDetectedVariable)
        self.targetDetailFrame.productDetectedLabel.grid(row = 0, column = 0)
        self.targetDetailFrame.productDetectedDisplay.grid(row = 0, column = 1)
        
        #Review List Frame
        self.reviewListFrame = tkinter.LabelFrame(self, bd = 2, relief = 'sunken', text = 'Reviews:')
        self.reviewListFrame.reviewList = tkinter.Listbox(self.reviewListFrame, width = 91, height = 8)
        self.reviewListFrame.reviewList.grid(row = 0, column = 0)
        self.reviewListFrame.reviewList.bind('<<ListboxSelect>>', self.updateReviewDetail)
        

        #Review Detail Frame
        self.reviewDetailFrame = tkinter.LabelFrame(self, bd = 2, relief = 'sunken', text = 'Review Detail:')

        self.reviewDetailFrame.pubDateLabel = tkinter.Label(self.reviewDetailFrame, text = 'Date Published:')
        self.reviewDetailFrame.pubDateVariable = tkinter.StringVar()
        self.reviewDetailFrame.pubDateDisplay = tkinter.Label(self.reviewDetailFrame, textvariable = self.reviewDetailFrame.pubDateVariable)
        self.reviewDetailFrame.pubDateDisplay.grid(row = 0, column = 0, sticky = 'w')
        
        self.reviewDetailFrame.ratingLabel = tkinter.Label(self.reviewDetailFrame, text = 'Rating:')
        self.reviewDetailFrame.ratingVariable = tkinter.StringVar()
        self.reviewDetailFrame.ratingDisplay = tkinter.Label(self.reviewDetailFrame, textvariable = self.reviewDetailFrame.ratingVariable)
        self.reviewDetailFrame.ratingLabel.grid(row = 1, column = 0, sticky = 'e')
        self.reviewDetailFrame.ratingDisplay.grid(row = 1, column = 1, sticky = 'w')
        
        self.reviewDetailFrame.fullReviewLabel = tkinter.Label(self.reviewDetailFrame, text = 'Full Review Text:')
        self.reviewDetailFrame.fullReviewText = tkinter.Text(self.reviewDetailFrame, width = 80, height = 20)
        self.reviewDetailFrame.fullReviewLabel.grid(row = 2, column = 0, sticky = 'e')
        self.reviewDetailFrame.fullReviewText.grid(row = 3, column = 1, sticky = 'w')

        #Render Frames
        self.targetFrame.grid(row = 0, column = 0, sticky = 'we')
        self.targetDetailFrame.grid(row = 1, column = 0, sticky = 'we')
        self.reviewListFrame.grid(row = 2, column = 0, sticky = 'we')
        self.reviewDetailFrame.grid(row = 3, column = 0, sticky = 'we')

        self.pack()


    def scrape(self):

        #Check if Entry is filled
        self.targetURL = self.targetFrame.targetVariable.get()
        if self.targetURL == '':
            messagebox.showerror('Launcher Error', 'No Target Specified!')
            return

        #Clear out old review list and full review text from previous target
        self.reviewListFrame.reviewList.delete(0, tkinter.END)
        self.reviewDetailFrame.fullReviewText.delete('1.0', tkinter.END)
        self.reviewDetailFrame.pubDateVariable.set('')
        self.reviewDetailFrame.ratingVariable.set('')
        
        #Attempt to retrieve page from server and parse
        try:

            self.targetPage = requests.get(self.targetURL)
            self.targetSoup = bs4.BeautifulSoup(self.targetPage.text, 'html.parser')
            
            #Parse bvseo-review format data into dictionary
            self.targetProductString = self.targetSoup.findAll({'meta' : 'content'})
            self.reviews = self.targetSoup.findAll('div', {'class':'bvseo-review'})
                     
            #master list of detected reviews of target with text values of corresponding tags parsed
            self.detectedReviews = []
        
            #Init temporary list to store each review's data and append list to master list
            for eachReview in self.reviews:
                
                tempReview = []

                rating = eachReview.findAll('span', {'itemprop':'ratingValue'})
                bestRating = eachReview.findAll('span', {'itemprop':'bestRating'})
                pubDate = eachReview.findAll('div', {'class':'bvseo-pubdate'})
                name = eachReview.findAll('span', {'itemprop':'name'})
                
                description = eachReview.findAll('span', {'itemprop':'description'})
                

                tempReview.append(int(rating[0].text))
                tempReview.append(int(bestRating[0].text))
                tempReview.append(str(pubDate[0].text))
                if str(name[0].text) == '':
                    tempReview.append('No Name')
                else:
                    tempReview.append(str(name[0].text))
                tempReview.append(str(description[0].text))

                self.detectedReviews.append(tempReview)
                self.reviewListFrame.reviewList.insert(0, tempReview[3])


            #Set product name in targetDetailFrame
            productName = self.reviews[0].findAll('meta', {'itemprop':'itemReviewed'})
            self.targetDetailFrame.productDetectedVariable.set(str(productName[0]['content']))

            #Add successfully scrapped URL to Combobox
            if (len(self.targetFrame.targetEntry['values'])) == 0 and (self.targetURL in self.targetFrame.targetEntry['values']) == False:
                startList = []
                startList.append(self.targetURL)
                self.targetFrame.targetEntry['values'] = startList
            elif (self.targetURL in self.targetFrame.targetEntry['values']) == False:
                tempList = self.targetFrame.targetEntry['values']
                tempTup = self.targetURL,
                tempList = tempList + tempTup
                self.targetFrame.targetEntry['values'] = tempList
            
   
        except Exception as e:
            #Error Catch in case request from server fails
            messagebox.showerror('Launcher Error', 'Invalid Target!\n\nDetails:\n'+str(e))
            return


    def updateReviewDetail(self, e):

        #Determine Selectoin and update reviewDetailFrame with selected review's data
        if self.reviewListFrame.reviewList.size() == 0: return
        self.highlightedReview = self.reviewListFrame.reviewList.curselection()
        self.reviewDetailFrame.pubDateVariable.set(self.detectedReviews[self.highlightedReview[0]][2])
        ratingString = str(self.detectedReviews[self.highlightedReview[0]][0]) + ' / ' + str(self.detectedReviews[self.highlightedReview[0]][1])
        self.reviewDetailFrame.ratingVariable.set(ratingString)
        self.reviewDetailFrame.fullReviewText.delete('1.0', tkinter.END)
        self.reviewDetailFrame.fullReviewText.insert('1.0', self.detectedReviews[self.highlightedReview[0]][4])
            


#Create, configure and launch application window
if __name__ == '__main__':
    
    newApp = tkinter.Tk()
    newApp.title('bvseoSpider-GUI: Customer Review Scraper v0.02A')

    bvSEOFrame(newApp)
