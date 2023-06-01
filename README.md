<a name="readme-top"></a>

# TerrapinTracker
> Aidan Henbest, Lisa Hunt, and Angelo Amato\
> Dr. Bixler\
> Senior Capstone-CS\
> 08 June 2023

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

### About
> Our plan is to create a website for Project Terrapin that regularly updates with the statistics on the growth of the hatchlings cared for both at MATES and other affiliated schools. We will use the measurement data for the growing terrapins and, using Python and JavaScript, create different graphs to display the data. This website will be public and linked to the main [Project Terrapin website](https://www.projectterrapin.org/). The site will update automatically when new data is added from recent measurements.
> Our project will help to raise awareness of the dangers that face the Northern Diamondback Terrapin species. They are a keystone species in the Barnegat Bay, meaning they are essential to the survival of the ecosystem. Our website will hopefully inspire others to get involved in the protection of terrapins, and potentially let them track the growth of hatchlings they may have found, giving them a more personal connection to the turtle(s) they helped to save.

### Built With
>  - [![Python](https://img.shields.io/badge/python-4381B2?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
>     - [![Pandas](https://img.shields.io/badge/pandas-130753?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
>     - [![Seaborn](https://img.shields.io/badge/Seaborn-454675.svg?style=for-the-badge&logo=data:image/png;base64,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&logoColor=white)](https://seaborn.pydata.org/)
>     - [![Matplotlib](https://img.shields.io/badge/Matplotlib-135474.svg?style=for-the-badge&logo=data:image/png;base64,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&logoColor=white)](https://matplotlib.org/)
>     - [![Django](https://img.shields.io/badge/django-092d1f?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
>  - [![HTML5](https://img.shields.io/badge/html5-e54d26?style=for-the-badge&logo=html5&logoColor=white)](https://en.wikipedia.org/wiki/HTML5)
>  - [![CSS3](https://img.shields.io/badge/css3-2a65f1?style=for-the-badge&logo=css3&logoColor=white)](https://en.wikipedia.org/wiki/CSS)
>  - [![MySQL](https://img.shields.io/badge/mysql-00618b?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
>  - [![Apache](https://img.shields.io/badge/apache-aa0000?style=for-the-badge&logo=apache&logoColor=white)](https://www.apache.org/)
>  - [![AWS](https://img.shields.io/badge/AWS-ff9901?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites
> txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation
> txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage
> txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Roadmap
> txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Contributing
>  txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### License
> txt
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Contact
>  Aidan Henbest - henbestaj@gmail.com\
>  Lisa Hunt - lhiusnat@gmail.com\
>  Angelo Amato - gangeloamato@gmail.com
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Acknowledgments
> We would like to thank Dr. Bixler, our teacher and mentor, for guiding us during this project. Their support and insights have been invaluable. We are grateful to the Marine Academy of Technology and Environmental Science for providing a conducive learning environment. Additionally, we appreciate Jon Gery's assistance in downloading the necessary software for our computers. Their contributions have greatly contributed to our success, and we express our sincere gratitude for their support.
<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- MARKDOWN LINKS & IMAGES -->
