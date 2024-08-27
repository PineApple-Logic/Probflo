## **Netica Risk Assessment Application for the Balule Catchment**

This is a web-based application designed for risk assessment in the Balule catchment area. The application is capable of generating a Netica `.cas` file based on data from expert surveys. Users can select the most likely case for each node thus setting values for Zero, Low, Medium, and High risk levels. The application then converts these results into a risk graph.

The application is coded in Python and utilizes the Netica C API. It offers an easy setup process using Docker, making deployment and management straightforward.

## Setup

```
git clone https://github.com/PineApple-Logic/Probflo.git
```
```
cd Probflo
docker build -t netica-probflo .
```

```
docker run -m 4g -c 4 -p 8502:8501 -d --restart unless-stopped netica-probflo
# Change the -m (memory) -c (cpu) values as needed.
```

- You can access it at http://localhost:8502
