import React from 'react';
import { Container, Row, Col, Card, Button, Breadcrumb } from 'react-bootstrap';
import { FaBed, FaCouch, FaShower, FaUtensils, FaWifi, FaSnowflake, FaTv, FaSuitcaseRolling } from 'react-icons/fa';


const HotelDetails = () => (
  
  <Container className="hotel-details">
    {/* Breadcrumb */}
    <Row>
      <Col>
        <Breadcrumb className="breadcrumb-custom mb-4">
          <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
          <Breadcrumb.Item active>Hotel Details</Breadcrumb.Item>
        </Breadcrumb>
      </Col>
    </Row>

    {/* Title and Location */}
    <Row className="text-center">
      <Col>
        <h2 className="hotel-title">Blue Origin Fams</h2>
        <p className="hotel-location">Galle, Sri Lanka</p>
      </Col>
    </Row>

    {/* Images */}
    <Row className="mt-4 align-items-stretch">
      <Col md={8}>
        <img
          src="/images/65046bf150d1abb7e5911702_x-65046bcfdc4f0.webp"
          alt="Hotel"
          className="img-fluid rounded main-image"
        />
      </Col>
      <Col md={4} className="d-flex flex-column justify-content-between">
        <img
          src="/images/hotel-del-coronado-views-suite-K1TOS1-K1TOJ1_2500x1100.jpg.webp"
          alt="Room"
          className="img-fluid rounded smaller-image"
        />
        <img
          src="/images/ihgor-member-rate-web-offers-1440x720.avif"
          alt="Bathroom"
          className="img-fluid rounded smaller-image mt-2"
        />
      </Col>
    </Row>


    {/* About Section and Booking Card */}
    <Row className="align-items-stretch mt-5">
    {/* About Section */}
    <Col md={8} className="d-flex flex-column justify-content-between">
      <div>
        <h4 className="about-title">About the place</h4>
        <p className="about-text">
          Minimal techno is a minimalist subgenre of techno music. It is
          characterized by a stripped-down aesthetic that exploits the use of
          repetition and understated development. Minimal techno is thought to
          have been originally developed in the early 1990s by Detroit-based
          producers Robert Hood and Daniel Bell.
        </p>
        <p className="about-text">
          Such trends saw the demise of the soul-infused techno that typified the
          original Detroit sound. Robert Hood has noted that he and Daniel Bell
          both realized something was missing from techno in the post-rave era.
        </p>
      </div>
    </Col>

    {/* Booking Card Section */}
    <Col md={4} className="d-flex align-items-start">
      <Card className="text-center p-4 shadow-sm rounded booking-card">
        <Card.Body>
          <h5 className="booking-title">Start Booking</h5>
          <div className="price-container">
            <span className="price-amount">$200</span>
            <span className="price-period"> per Day</span>
          </div>
          <Button variant="primary" className="mt-3 booking-button">
            Book Now!
          </Button>
        </Card.Body>
      </Card>
    </Col>
  </Row>

  
    {/* Room Amenities */}
    <Container fluid className="px-5 mt-4">
    <Row className="text-center amenities-row">
      {[
        { text: '1 bedroom', icon: <FaBed /> },
        { text: '1 living room', icon: <FaCouch /> },
        { text: '1 bathroom', icon: <FaShower /> },
        { text: '1 dining room', icon: <FaUtensils /> },
        { text: '10 mbp/s', icon: <FaWifi /> },
        { text: '7 unit ready', icon: <FaSuitcaseRolling /> },
        { text: '1 refrigerator', icon: <FaSnowflake /> },
        { text: '2 television', icon: <FaTv /> },
      ].map((amenity, index) => (
        <Col key={index} className="amenity">
          <div className="amenity-icon">{amenity.icon}</div>
          <p className="amenity-text">{amenity.text}</p>
        </Col>
      ))}
    </Row>
  </Container>

    {/* Treasure to Choose Section */}
    <div className="footer-spacing">
    <div className="treasure-to-choose mt-5">
    <h4 className="section-title">Treasure to Choose</h4>
    <Row className="mt-3">
      {[
        { title: 'Green Lake', subtitle: 'Nature', img: 'images/GettyImages-510168546-c53a5315c16b47379271d8c83baabaaf.jpg' },
        { title: 'Dog Clubs', subtitle: 'Pool', img: 'images/shutterstock_2205974177.jpg;w=960.jpeg' },
        { title: 'Labour and Wait', subtitle: 'Shopping', img: 'images/homepage-carousel-image-2_1.webp.jpeg', badge: 'Popular Choice' },
        { title: 'Snorkeling', subtitle: 'Beach', img: 'images/AdobeStock_654868587-min.jpeg.webp' },
      ].map(({ title, subtitle, img, badge }, idx) => (
        <Col key={idx} md={3} className="mb-3">
          <Card className="custom-card">
            <div className="card-image-wrapper">
              {badge && <span className="badge-custom">{badge}</span>}
              <Card.Img variant="top" src={img} className="card-img" />
            </div>
            <Card.Body>
              <Card.Title className="card-title">{title}</Card.Title>
              <Card.Text className="card-subtitle">{subtitle}</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  </div>
  </div>

  </Container>
);

export default HotelDetails;
