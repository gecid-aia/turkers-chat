import React from 'react';
import PropTypes from 'prop-types';

export default class FilterMessagesIcon extends React.Component {
  static propTypes = { filterTurkersMessages: PropTypes.bool.isRequired }
  static defaultProps = { filterTurkersMessages: false };

  render() {
    const { filterTurkersMessages } = this.props;
    return (
      <img
        src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAOCAYAAAA1+Nx+AAAABHNCSVQICAgIfAhkiAAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hvdO8Dvz4AAAAmdEVYdENyZWF0aW9uIFRpbWUAcXVhIDI2IGZldiAyMDIwIDE3OjM3OjAy3+qW7AAAAKpJREFUOI1j/P///38GGgIWbILLli1j2Lt3L9mGlpWVMairq0M4/7GAnJyc/wwMDGTj/fv3w81iItuZRAJGbHFw5swZhps3b5JtqKurK4OYmBhuC6gJWFasWMGwdu1aqhra2NjIoKWlBeFUVVVRFKHYMH0j+caNG/9v375NVUMtLS0ZhIWFIRYMSE5GB319fQw7d+4k2tDu7m4GPT09CAdbTkYHiYmJgzeSASNUvQzaK2+nAAAAAElFTkSuQmCC"
        title={filterTurkersMessages ? 'All messages' : 'See turkers messages only'}
        alt={filterTurkersMessages ? 'All messages' : 'See turkers messages only'}
      />
    )
  }
}
