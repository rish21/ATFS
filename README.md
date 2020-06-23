## _Assistive Technology to Study STEM Subjects for Visually Impaired People_

---

#### An MEng Individual Project for the Degree of Electrical and Electronic Engineering with Management
#### Imperial College London
#### Department of Electrical and Electronic Engineering
###### Completed in the Summer of 2020

---

##### ABSTRACT

The WHO reports with confidence that there are currently over 2 billion people in the world who have some form of visual impairment or blindness. Over 30 million have severe impairment and over 1 million of those are children under the age of 15. These individuals face several unprecedented challenges, one these being education. Advances in hardware and software have paved the way for many solutions both simple and complex; from text enlargers to braille translation devices. However, these solutions are not adequate for students wishing to study more complex STEM subjects. Interpreting information with items such as graphs and tables is extremely difficult. This problem is further heightened, as much of the national curriculum still uses dated non-digital paper material; resources and equipment have also become exceedingly expensive and made it difficult for enough teachers to be properly trained. This project tackled this problem by developing a system that incorporated computer vision and machine learning technologies, to enable students to study and pursue a passion for STEM subjects. It scans the literature of interest and extracts all the information present within it. Graphs, tables, images, equations and text are all converted into speech or audio that can be interpreted and understood by the student. They can navigate a virtual interface using a joystick controller to access all this information. User testing proved that this system was effective at extracting and presenting the information to the user, enabling them to study and answers questions from the material. The simple intuitive virtual interface also made it quick and easy to learn and train students and teachers; all while being considerably cheaper than current solutions and methods. 

##### Requirements

Python3.6 and an Xbox 360 Controller are **necessary** to run and operate this system.

Please place your Google Cloud Service Account Key within `src` and place your the file name, Mathpix and ExtractTable/CamelotPro IDD and Key within the `src/standard.JSON` file.

You can get your keys here:

Mathpix - https://dashboard.mathpix.com/ 
CamelotPro/ExtractTable - https://extracttable.com/camelotpro.html 
Google Cloud Service Account Key - https://cloud.google.com/iam/docs/creating-managing-service-account-keys 

The `requirements.txt` file lists all Python dependencies, and they should be installed using:

```python
pip install -r requirements.txt
```

##### Run

Ensure you are in the `src` directory and run:

```python
python main.py
```

##### Examples

The raw outputs from the examples used in the final report in the Testing Section (Section 5), are availble to view in the `examples` folder


###### Notes

+ The repository contains some additional files and code that are related the presentation given for this project
