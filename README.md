# ORPO Belarusian agent
The program reads the source pdf file, compiles questions, answers and dummy answers from the text of the file, translates it into Belarusian language and saves the results into a csv file. The resulting information can be used as input for the ORPO model training process and should help the model to better understand the data from the source.

# Installation

git clone https://github.com/yuragorlo/orpo-bel-agent.git \
cd orpo-bel-agent \
python3 -m venv venv \
source ./venv/bin/activate \
pip3 install -r requirements.txt \
mv example.env .env # add your own API key to .env file

# Run
cd src \
python3 main.py