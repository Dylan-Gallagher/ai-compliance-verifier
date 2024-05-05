jest.mock('react-vis-network-graph', () => ({
  // Your mock implementation for react-vis-network-graph here
}));

jest.mock('react-pdftotext', () => ({
  // Your mock implementation for react-pdftotext here
  __esModule: true, // this property makes it work
  default: () => {
    // Return whatever the module should return
    return Promise.resolve('mocked text');
  },
}));

import { render } from '@testing-library/react';
import App from './App';

test('renders without crashing', () => {
  expect(() => render(<App />)).not.toThrow();
});