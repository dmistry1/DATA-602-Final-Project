import React, { useState, useEffect } from 'react';
import "bootstrap-icons/font/bootstrap-icons.css";
import './App.css';
import DatePicker from "react-datepicker";
import Button from 'react-bootstrap/Button';
import "react-datepicker/dist/react-datepicker.css";
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Spinner from 'react-bootstrap/Spinner';

function App() {
  const [currentDateMinusTwo, setCurrentDateMinusTwo] = useState(null);
  const [selectedDate, setSelectedDate] = useState('2023-08-08');
  const [mapHtml, setMapHtml] = useState();
  const [historicalMapHtml, setHistoricalMapHtml] = useState('');
  const [loading, setLoading] = useState(true);

  // Gets the Active fire map
  useEffect(() => {
    setLoading(true)
    fetch('https://maui-wildfire-wddg2qmg6a-ue.a.run.app').then(res => res.text()).then(mapHtml => {
      setMapHtml(mapHtml)
    });
    setLoading(false)
  }, []);

  useEffect(() => {
    sendDataToBackend(selectedDate)
  }, [])
  // Gets the Current date and subtracts 2 from it
  useEffect(() => {
    // Get the current date
    const today = new Date();
    const twoDaysAgo = new Date(today);
    twoDaysAgo.setDate(today.getDate() - 2);

    setCurrentDateMinusTwo(twoDaysAgo);
  }, []);

  // Formants the selected date.
  const handleDateChange = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    console.log(`${year}-${month}-${day}`)
    setSelectedDate(`${year}-${month}-${day}`);
  }

  // onClick handler that will get historical fire map
  const sendDataToBackend = async () => {
    try {
      const response = await fetch('https://maui-wildfire-wddg2qmg6a-ue.a.run.app/historical_fire', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selectedDate: selectedDate }),
      });

      if (response.ok) {
        const responseData = await response.text()
        setHistoricalMapHtml(responseData)
      } else {
        console.error('Failed to send data');
      }
    } catch (error) {
      console.error('Error sending data:', error);
    }
  }

  return (
    <div className="maui-wildfire">
      <header className="App-header">
        <h1 className='page-title mt-2'>
          Maui Wildfires
          <i className="fire-icon bi bi-fire"></i>
        </h1>
      <CardGroup className="mb-2">
      {/* Renders the About card */}
        <Card>
          <Card.Body>
            <Card.Title>
              <h1 className='title'>About</h1>
              <hr/>
              </Card.Title>
            <Card.Text>
            <span className="text">
              This project shows the number of active fires in Maui and predicts if weather conditions are likely to produce active fires.
              This utilizes satellite data from the NASA Fire Information for Resource Management System
              (<a href='https://firms.modaps.eosdis.nasa.gov/' target="_blank">FIRM</a>) 
              and weather data from the National Oceanic and Atmospheric Administration(<a href='https://www.noaa.gov/' target="_blank">NOAA</a>)
            </span>
            </Card.Text>
          </Card.Body>
        </Card>
      </CardGroup>
      <CardGroup>
      {/* Renders the Active fire card */}
      <Card>
        <Card.Body>
          <Card.Title>
          <h1 className='title'>Active Fire</h1>
          <hr/>
          </Card.Title>
          <span className='text'>This map repersents active fires in Maui and predicts if an active fire is likely to occur.</span>
          <div >
            {currentDateMinusTwo && (
              <span className='small-text'>Showing map for: {currentDateMinusTwo.toLocaleDateString()}</span>
            )}
          </div>
          <div>
          {loading ? (
          <Spinner animation="border" role="status">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
          ): (
            <div className="pt-4" dangerouslySetInnerHTML={{ __html: mapHtml }} />
          )}
          </div>
        </Card.Body>
      </Card>
      {/* Renders the Historical Fire card */}
      <Card>
        <Card.Body>
          <h1 className='title'>Historical Fire</h1>
          <hr/>
          <Card.Text>
          <span className='text'>Search for any days within the past year to see the active fires across Maui</span>
          </Card.Text>
          <DatePicker
          className='date-picker '
          minDate={new Date('08-08-2023')}
          maxDate={currentDateMinusTwo}
          dateFormat="yyyy-MM-dd"
          showMonthDropdown
          showYearDropdown
          peekNextMonth
          placeholderText='Select date...'
          value={selectedDate}
          onChange={handleDateChange}
        >
        </DatePicker>
        {/* Renders the Show Fire Map Button */}
          <Button
            className='button'
            onClick={sendDataToBackend}
          >
            Show Fire Map
          </Button>
        <div className="pt-2" dangerouslySetInnerHTML={{ __html: historicalMapHtml }} />
        </Card.Body>
      </Card>
    </CardGroup>
      </header>
    </div>
      
  );
}

export default App;
