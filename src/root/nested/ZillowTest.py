'''
Created on Jul 1, 2014

@author: kahere
'''

from root.nested.ZillowZip import ZipData, AddressData
import pandas
import numpy as np
import tkinter
import tkinter.filedialog as tkFileDialog
import os

def zips():
    # Get list of zip codes from csv file
    zip_list = pandas.DataFrame().from_csv(r'C:\Python code\ZillowTest\src\root\nested\zip_code_database.csv')
    
    # Select state to test
    zips = zip_list[zip_list.state=='FL'].index
    print (zips)
    zips = zips[:5]
    
    home_values = pandas.DataFrame(index=zips,columns=['Zillow_Home_Value_Index','Median_Single_Family','Median_Condo','Median_2bd','Median_3bd','Median_4bd','Median_PerSqFt','State'])
    for i in zips:
        # Loop through zip code list, extracting home value data at each zip code
        getzip = ZipData(i)
        
        try:
            get_values = getzip.returnHomeValues()
            home_values.ix[i,:-1] = get_values
            home_values.ix[i,-1] = getzip.returnState()
        except AttributeError:
            print (i)
            continue
                
    print (home_values)
    
def address(address, test_zipcode):
    # Call AddressData class methods
    address_data = AddressData(address, test_zipcode)
    results = address_data.get_deep_search_results()

    if results is not None:
        # Set address attributes. If not available, default value is 0
        try:
            street_address = results.result.address.street.contents[0]
        except AttributeError:
            street_address = 0
        try:
            city = results.result.address.city.contents[0]
        except AttributeError:
            city = 0
        try:
            state = results.result.address.state.contents[0]
        except AttributeError:
            state = 0
        try:
            zipcode = results.result.address.zipcode.contents[0]
        except AttributeError:
            zipcode = 0
        try:
            latitude = results.result.latitude.contents[0]
        except AttributeError:
            latitude = 0
        try:
            longitude = results.result.longitude.contents[0]
        except AttributeError:
            longitude = 0
        try:
            property_type = results.result.useCode.contents[0]
        except AttributeError:
            property_type = 0
        try:
            tax_assessment = results.result.taxAssessment.contents[0]
        except AttributeError:
            tax_assessment = 0
        try:
            year_built = results.result.yearBuilt.contents[0]
        except AttributeError:
            year_built = 0
        try:
            lot_size = results.result.lotSizeSqFt.contents[0]
        except AttributeError:
            lot_size = 0
        try:
            sq_ft = results.result.finishedSqFt.contents[0]
        except AttributeError:
            sq_ft = 0
        try:
            bedrooms = results.result.bedrooms.contents[0]
        except AttributeError:
            bedrooms = 0
        try:
            bathrooms = results.result.bathrooms.contents[0]
        except AttributeError:
            bathrooms = 0
        try:
            estimated_mkt_value = results.result.zestimate.amount.contents[0]
        except (AttributeError, IndexError):
            estimated_mkt_value = 0
            
        dataset = np.array([street_address,city,state,zipcode,latitude,longitude,property_type,tax_assessment,year_built,lot_size,sq_ft,bedrooms,bathrooms,estimated_mkt_value])
        dataset = dataset.reshape((1,np.shape(dataset)[0]))    
        return dataset
    
    else:
        return

def selectFile():
    # Browse to directory of portfolio file
    root2 = tkinter.Tk()
    root2.withdraw()
    currdir = os.getcwd()
    validfile = False
    while validfile == False: 
        tempdir = tkFileDialog.askopenfilename(parent=root2, initialdir=currdir, title='Please select a portfolio .csv file. Cancel produces equal exposures in each state/province.')

        # Make sure file is correct type
        if tempdir.endswith('.csv'):
            portfolio_file = tempdir
            validfile = True
        else:
            print("Error: File type must be .csv.")      
    return portfolio_file             

if __name__ == '__main__':    
    
#     zips()

    # .csv file should have 4 columns (with headers): Address, City, State, Zip
    file_name = selectFile()
    
    # Attributes to collect from Zillow
    column_list = columns=['street_address','city','state','zipcode','latitude','longitude','property_type','tax_assessment','year_built','lot_size','sq_ft','bedrooms','bathrooms','estimated_mkt_value']
    
    # Load text file
    address_list = np.loadtxt(file_name,delimiter=',',skiprows=1,dtype=str)
    
    # Check each record to see if Zillow can find it, add results to address_info dataframe
    address_info = pandas.DataFrame(columns=column_list)
    for row in address_list:
        single_address = row[0][2:-1]+' '+row[1][2:-1]+' '+row[2][2:-1]
        zipcode = row[-1][2:-1]
        
        # Excel removes leading 0, this adds them back
        if len(str(zipcode)) < 5:
            zipcode = str(zipcode).zfill(5)    
        
        get_address = pandas.DataFrame(address(single_address,zipcode),columns=column_list)
        address_info = address_info.append(get_address)

    # Output address dataframe to .csv file
    address_info.to_csv('address_test.csv',sep=',',index=False)
        
