import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';

import { AuthProvider, useAuth } from './src/contexts/AuthContext';
import { RootStackParamList } from './src/types';

import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import CoffeeListScreen from './src/screens/CoffeeListScreen';
import AddCoffeeScreen from './src/screens/AddCoffeeScreen';
import EditCoffeeScreen from './src/screens/EditCoffeeScreen';
import PurchaseHistoryScreen from './src/screens/PurchaseHistoryScreen';

const Stack = createStackNavigator<RootStackParamList>();

const AppNavigation: React.FC = () => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#8B4513" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}
      >
        {user ? (
          <>
            <Stack.Screen 
              name="CoffeeList" 
              component={CoffeeListScreen}
              options={{ title: 'Cafés' }}
            />
            <Stack.Screen 
              name="AddCoffee" 
              component={AddCoffeeScreen}
              options={{ title: 'Adicionar Café' }}
            />
            <Stack.Screen 
              name="EditCoffee" 
              component={EditCoffeeScreen}
              options={{ title: 'Editar Café' }}
            />
            <Stack.Screen 
              name="PurchaseHistory" 
              component={PurchaseHistoryScreen}
              options={{ title: 'Histórico' }}
            />
          </>
        ) : (
          <>
            <Stack.Screen 
              name="Login" 
              component={LoginScreen}
              options={{ title: 'Login' }}
            />
            <Stack.Screen 
              name="Register" 
              component={RegisterScreen}
              options={{ title: 'Cadastro' }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <StatusBar style="dark" />
      <AppNavigation />
    </AuthProvider>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
});

export default App;
