import { render, screen } from '@testing-library/react';
import App from './App';

test('renders SentinelPay header', () => {
  render(<App />);
  const headerElement = screen.getByText(/SentinelPay - AI Trust Detector/i);
  expect(headerElement).toBeInTheDocument();
});
