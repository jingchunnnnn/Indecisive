export type BrowserLocation = {
  lat: number;
  lng: number;
};

export function requestBrowserLocation(): Promise<BrowserLocation> {
  if (typeof navigator === "undefined" || !navigator.geolocation) {
    return Promise.reject(new Error("Location is not available in this browser."));
  }

  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          lat: position.coords.latitude,
          lng: position.coords.longitude
        });
      },
      (error) => {
        if (error.code === error.PERMISSION_DENIED) {
          reject(new Error("Location permission was denied. Please allow location to find nearby food."));
          return;
        }
        reject(new Error("We could not get your location. Please try again."));
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 60000
      }
    );
  });
}
