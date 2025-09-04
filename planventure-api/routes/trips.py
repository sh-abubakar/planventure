from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.trip import Trip
from models.user import User
from database import db
from utils.middleware import auth_required, require_user_ownership, get_current_user
from utils.itinerary import generate_default_itinerary, get_itinerary_suggestions
from datetime import datetime

trips_bp = Blueprint('trips', __name__, url_prefix='/api/trips')

@trips_bp.route('/', methods=['GET'])
@auth_required
def get_user_trips():
    """Get all trips for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        trips = Trip.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'trips': [trip.to_dict() for trip in trips],
            'count': len(trips)
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch trips', 'error': str(e)}), 500

@trips_bp.route('/', methods=['POST'])
@auth_required
def create_trip():
    """Create a new trip for the authenticated user."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        required_fields = ['destination', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        if start_date > end_date:
            return jsonify({'message': 'Start date must be before end date'}), 400
        
        # Generate itinerary if not provided
        itinerary = data.get('itinerary')
        if not itinerary:
            trip_type = data.get('trip_type', 'leisure')  # Default to leisure
            itinerary = generate_default_itinerary(
                destination=data['destination'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                trip_type=trip_type
            )
        
        # Create new trip
        trip = Trip(
            user_id=user_id,
            destination=data['destination'],
            start_date=start_date,
            end_date=end_date,
            itinerary=itinerary
        )
        
        # Set coordinates if provided
        if 'latitude' in data and 'longitude' in data:
            trip.set_coordinates(data['latitude'], data['longitude'])
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip': trip.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create trip', 'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@auth_required
@require_user_ownership('user_id')
def get_trip(trip_id):
    """Get a specific trip by ID (user can only access their own trips)."""
    try:
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'message': 'Trip not found'}), 404
        
        return jsonify({'trip': trip.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch trip', 'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@auth_required
def update_trip(trip_id):
    """Update a specific trip (user can only update their own trips)."""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'message': 'Trip not found'}), 404
        
        # Check ownership
        if trip.user_id != user_id:
            return jsonify({'message': 'Access denied: You can only update your own trips'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        # Update fields if provided
        if 'destination' in data:
            trip.destination = data['destination']
        
        if 'start_date' in data:
            try:
                trip.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
        
        if 'end_date' in data:
            try:
                trip.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
        
        if 'itinerary' in data:
            trip.itinerary = data['itinerary']
        
        if 'latitude' in data and 'longitude' in data:
            trip.set_coordinates(data['latitude'], data['longitude'])
        
        # Validate dates
        if trip.start_date > trip.end_date:
            return jsonify({'message': 'Start date must be before end date'}), 400
        
        trip.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Trip updated successfully',
            'trip': trip.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update trip', 'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@auth_required
def delete_trip(trip_id):
    """Delete a specific trip (user can only delete their own trips)."""
    try:
        user_id = get_jwt_identity()
        trip = Trip.query.get(trip_id)
        
        if not trip:
            return jsonify({'message': 'Trip not found'}), 404
        
        # Check ownership
        if trip.user_id != user_id:
            return jsonify({'message': 'Access denied: You can only delete your own trips'}), 403
        
        db.session.delete(trip)
        db.session.commit()
        
        return jsonify({'message': 'Trip deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete trip', 'error': str(e)}), 500

@trips_bp.route('/itinerary-suggestions', methods=['POST'])
@auth_required
def get_itinerary_suggestions_route():
    """Get itinerary suggestions for a destination."""
    try:
        data = request.get_json()
        
        if not data or 'destination' not in data:
            return jsonify({'message': 'Destination is required'}), 400
        
        destination = data['destination']
        start_date = data.get('start_date', '2024-10-15')
        end_date = data.get('end_date', '2024-10-20')
        
        suggestions = {}
        trip_types = ['leisure', 'business', 'adventure', 'family']
        
        for trip_type in trip_types:
            suggestions[trip_type] = generate_default_itinerary(
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                trip_type=trip_type
            )
        
        return jsonify({
            'destination': destination,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to generate suggestions', 'error': str(e)}), 500

@trips_bp.route('/generate-itinerary', methods=['POST'])
@auth_required
def generate_itinerary_route():
    """Generate a single itinerary based on specific parameters."""
    try:
        data = request.get_json()
        
        required_fields = ['destination', 'start_date', 'end_date']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        trip_type = data.get('trip_type', 'leisure')
        
        itinerary = generate_default_itinerary(
            destination=data['destination'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            trip_type=trip_type
        )
        
        return jsonify({
            'destination': data['destination'],
            'trip_type': trip_type,
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'itinerary': itinerary
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to generate itinerary', 'error': str(e)}), 500
