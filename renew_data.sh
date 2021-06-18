echo "Fetching sciensano data"
python3 data_fetch/sciensano/sciensano.py
echo "Fetched sciensano data"
echo "Fetching Google mobility data"
python3 data_fetch/google_mobility/google_mobility.py
echo "Fetched Google mobility data"

echo "Processing cases / deaths"
python3 data_processors/sciensano/cases_deaths.py
echo "Done processing cases / deaths"
echo "Processing hospitalisations"
python3 data_processors/sciensano/hospitalisations.py
echo "Done processing hospitalisations"
echo "Processing tests"
python3 data_processors/sciensano/tests.py
echo "Done processing tests"

echo "Processing kmeans data"
python3 data_processors/kmeans/kmeans.py
echo "Done processing kmeans data"

echo "Processing Google mobility data"
python3 data_processors/mobility/mobility.py
echo "Done processing Google mobility data"

echo "Running kmeans"
python3 algorithms/kmeans/script.py
echo "Finished kmeans"
echo "Running neural network"
python3 algorithms/neural_network/script.py
echo "Finished running neural network"