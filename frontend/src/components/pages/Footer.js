import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './edits.css';


const Footer = () => (
<div className="content">
<div className="footer-container">
    <Container>
      <Row className="align-items-center">
        <Col md={6}>
          <h2 className="footer-logo highlight">Campus<span className="highlight1">Vacay.</span></h2>
          <p className="footer-text">
            We kaboom your beauty holiday instantly and memorable.
          </p>
        </Col>
        <Col md={6} className="text-end">
          <h5>Become hotel Owner</h5>
          <Button variant="primary" className="footer-button">
            Register Now
          </Button>
        </Col>
      </Row>
    </Container>
    </div>
    <div className="footer">
      <p>Copyright 2024 • All rights reserved • CampusVacay.</p>
    </div>
  </div>
);

export default Footer;
