import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import React from 'react';

const Title = ({ children }) => (
  <Typography color="primary" component="h2" gutterBottom variant="h6">
    {children}
  </Typography>
);

Title.propTypes = {
  children: PropTypes.element.isRequired,
};

export default Title;
