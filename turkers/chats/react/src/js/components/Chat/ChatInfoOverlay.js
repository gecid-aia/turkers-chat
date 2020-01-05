import React from 'react';
import PropTypes from 'prop-types';

export default class ChatBox extends React.Component {
  static propTypes = {
    text: PropTypes.string.isRequired,
  }

  render(){
    const { text } = this.props;

    return (
      <div className="info-overlay">
        {text}
      </div>
    );
  };
}
